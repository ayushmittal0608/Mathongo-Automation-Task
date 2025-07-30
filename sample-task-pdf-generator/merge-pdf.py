import os
import base64
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

PDF_PANEL_URL = "http://localhost:3002/pdf-panel"
DB_FOLDER = "db"
DOWNLOAD_DIR = "downloaded_pdfs"
OUTPUT_MERGED_DIR = "merged_pdfs"

CHROME_USER_DATA_DIR = os.path.abspath("C:\\selenium_chrome_profile")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_MERGED_DIR, exist_ok=True)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


driver.set_script_timeout(120)

def wait_for_content_load(driver_instance, timeout=60):
    """
    Waits for the main content container (#page) to be present,
    then explicitly waits for 20 seconds for MathJax and other dynamic content to render.
    """
    print(f"[{driver_instance.current_url}] Waiting for main content container ('#page') to appear...")
    try:
        WebDriverWait(driver_instance, timeout).until(
            EC.presence_of_element_located((By.ID, "page"))
        )
        print(f"[{driver_instance.current_url}] Main content container ('#page') is present.")

        print(f"[{driver_instance.current_url}] Giving MathJax and other content time to render (20 seconds).")
        time.sleep(20) 
        
        print(f"[{driver_instance.current_url}] Content (including MathJax) should be loaded.")
    except Exception as e:
        print(f"[{driver_instance.current_url}] Error or timeout waiting for initial content container ({e}). Falling back to 20-second sleep.")
        time.sleep(20)

def print_page_to_pdf_cdp(driver_instance, filename_prefix):
    print(f"[{driver_instance.current_url}] Generating PDF using CDP...")
    
    print_options = {
        'landscape': False,
        'displayHeaderFooter': False,
        'printBackground': True,
        'preferCSSPageSize': True, 
        'marginTop': 0.4,
        'marginBottom': 0.4,
        'marginLeft': 0.4,
        'marginRight': 0.4,
    }
    
    result = driver_instance.execute_cdp_cmd("Page.printToPDF", print_options)
    
    pdf_data = base64.b64decode(result['data'])
    
    output_path = os.path.join(DOWNLOAD_DIR, f"{filename_prefix}.pdf")
    with open(output_path, "wb") as f:
        f.write(pdf_data)
    print(f"CDP-generated PDF saved to: {output_path}")
    return output_path


try:
    json_files = [f for f in os.listdir(DB_FOLDER) if f.endswith('.json')]
    print(f"Found JSON files: {json_files}")

    for json_file in json_files:
        input_name = os.path.splitext(json_file)[0]
        print(f"\nProcessing: {input_name}")

        driver.get(PDF_PANEL_URL)
        print(f"Navigated to {PDF_PANEL_URL}")

        try:
            input_field = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "form-control"))
            )
            input_field.clear()
            input_field.send_keys(input_name)
            print("Entered input.")

            original_window = driver.current_window_handle

            generate_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Generate"))
            )
            generate_button.click()
            print("Clicked 'Generate'.")

            question_window = None
            try:
                print(f"[{driver.current_url}] Waiting for a new window to open for up to 90 seconds...")
                WebDriverWait(driver, 90).until(EC.new_window_is_opened(driver.window_handles))
                
                all_handles = driver.window_handles
                
                for handle in all_handles:
                    if handle != original_window:
                        driver.switch_to.window(handle)
                        current_url = driver.current_url
                        current_title = driver.title 
                        print(f"Switched to potential new window: {handle} (URL: {current_url}, Title: {current_title})")
                        
                        if "http://localhost:3002/question" in current_url or "question_marks" in current_title:
                            question_window = handle
                            print(f"Confirmed: This is the question window.")
                            break # Found the correct window, exit loop
                        else:
                            # If it's not the question window, close it (might be an unwanted pop-up)
                            print(f"Unexpected window. Closing: {handle}")
                            driver.close()
                            driver.switch_to.window(original_window) # Switch back to original to continue search if needed
                
            except Exception as e:
                print(f"Timeout or error while waiting for/identifying new window: {e}")
                print(f"Current window handles: {driver.window_handles}")
                # Attempt to close any extra windows and continue
                for handle in driver.window_handles:
                    if handle != original_window:
                        try: driver.switch_to.window(handle); driver.close()
                        except: pass
                driver.switch_to.window(original_window)
                continue # Skip to next JSON file

            if not question_window:
                print("\nFINAL ERROR: Could not find the 'question' window after panel generation.")
                # Attempt to close any remaining pop-up windows before continuing
                for handle in driver.window_handles:
                    if handle != original_window:
                        try: driver.switch_to.window(handle); driver.close()
                        except: pass
                driver.switch_to.window(original_window)
                continue # Skip to next JSON file

            # --- Process question_marks window to add solutions ---
            driver.switch_to.window(question_window)
            print("Switched to question_marks window.")
            wait_for_content_load(driver) # Wait for initial questions to render

            # Inject JavaScript to append solutions to the #page div
            inject_solution_script = """
            (function() {
                let jsonData = sessionStorage.getItem('json');
                if (!jsonData) {
                    console.error('JSON data not found in sessionStorage.');
                    return;
                }
                jsonData = JSON.parse(jsonData);

                const pageDiv = document.getElementById('page');
                if (!pageDiv) {
                    console.error('Page div with ID "page" not found.');
                    return;
                }
                if (pageDiv) {
                    pageDiv.innerHTML = ''; // Option 1: remove all existing content
                    // Or use this line to hide it instead of removing:
                    // pageDiv.style.display = 'none';
                }

                
                
                for (let i = 0; i < jsonData.length; i++) {
                    const questionData = jsonData[i];
                    
                    // Find the question element this solution should follow
                    // This is a bit tricky; we'll append to the main 'page' div directly
                    // or try to find the last element of the current question.
                    // For simplicity, let's append to the page div with a clear heading.

                    let solutionText = questionData.solution.text;
                    let options = questionData.options || [];
                    let answer = ' ';
                    if (typeof solutionText !== 'string') {
                        solutionText = JSON.stringify(solutionText);
                    }
                    
                    if(questionData.correctValue!=null){
                        answer+=questionData.correctValue;
                    }
                    else{
                        for(let i=0; i<options.length; i++){
                            if(options[i].isCorrect){
                                answer+=options[i].text;
                            }
                        }
                    }
                    
                    let optionsHTML = '';
                    if (Array.isArray(options) && options.length > 0) {
                    
                    for (let i = 0; i < options.length; i++) {
                        const opt = options[i];
                        // Use A, B, C, D...
                        const label = String.fromCharCode(65 + i);
                        optionsHTML += `<span><strong>${label}.</strong> ${opt.text}</span><br>`;
                    }
                    } else {
                    optionsHTML = ' ';
                    }


                    const solutionHtml = `
                        <div class="col-12 mt-4 mb-1" style="page-break-before: auto;">
                            <h3>Q${i + 1}. ${questionData.question.text}</h3>
                            <span>${optionsHTML}</span>
                        </div>
                        <div class="col-12 mb-5">
                            <span>Ans: </strong>${answer}</span><br>
                            Solution: ${solutionText.replace(/\\n/g, '<br>')}
                        </div>
                    `;
                    pageDiv.insertAdjacentHTML('beforeend', solutionHtml);
                }

                // Re-typeset MathJax for the newly added content
                if (window.MathJax && window.MathJax.Hub) {
                    window.MathJax.Hub.Queue(['Typeset', window.MathJax.Hub]);
                    console.log('MathJax re-typeset triggered for solutions.');
                } else {
                    console.warn('MathJax not found or not ready for re-typesetting.');
                }
            })();
            """
            driver.execute_script(inject_solution_script)
            print("Injected JavaScript to add solutions to the question page.")

            print("Giving time for injected solutions and MathJax to render (20 seconds).")
            time.sleep(20)

            combined_pdf_path = print_page_to_pdf_cdp(driver, input_name) # Name the PDF after the input_name
            
            final_output_path = os.path.join(OUTPUT_MERGED_DIR, f"{input_name}.pdf")
            os.rename(combined_pdf_path, final_output_path)
            print(f"Final combined PDF saved as: {final_output_path}")

            if question_window:
                try: 
                    driver.switch_to.window(question_window)
                    driver.close()
                    print(f"Closed question window {question_window}.")
                except Exception as close_e: 
                    print(f"Error closing question window {question_window}: {close_e}")
            
            driver.switch_to.window(original_window)
            print(f"Switched back to original window: {original_window}")

        except Exception as e:
            print(f"An unexpected error occurred during processing for {input_name}: {e}")
            try:
                driver.switch_to.window(original_window)
            except:
                if driver.window_handles:
                    driver.switch_to.window(driver.window_handles[0])

            for handle in driver.window_handles:
                if handle != driver.current_window_handle:
                    try:
                        driver.switch_to.window(handle)
                        driver.close()
                    except Exception as close_e:
                        print(f"Error closing window {handle} during error cleanup: {close_e}")
            try: 
                driver.switch_to.window(original_window)
            except:
                pass 

finally:
    driver.quit()
    print("Browser closed.")