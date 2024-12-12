import time
import pyautogui
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

# Define the directory to save the screenshot and downloaded image
screenshot_dir = os.getcwd()  # Current working directory
download_dir = os.path.join(screenshot_dir, "downloaded_file")  # Temporary directory to save the image

# Ensure the downloaded_file directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Initialize global variables
driver = None
switch_clicked = False

# Function to take a screenshot, convert it to PNG, and save it to the directory
def capture_screenshot():
    global driver

    if driver is None:
        # Set up Chrome options to disable GPU and hardware acceleration
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")  # Disable GPU acceleration
        options.add_argument("--disable-software-rasterizer")  # Additional option to prevent GPU issues
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Capture the screen
    screenshot = pyautogui.screenshot()
    screenshot_path = os.path.join(screenshot_dir, "screenshot.png")

    # Save the screenshot as PNG
    screenshot.save(screenshot_path)
    print(f"Screenshot saved to: {screenshot_path}")

    # Open a new tab in the existing driver
    driver.execute_script("window.open('https://translate.yandex.com/en/ocr');")
    driver.switch_to.window(driver.window_handles[-1])

    # Wait for the page to load
    time.sleep(2)
    
    # Now, upload the image to Google Translate and get translated text
    upload_image_to_translate(screenshot_path)

# Function to upload the image to Google Translate for processing
def upload_image_to_translate(image_path):
    global driver, switch_clicked

    # Step 2: Wait for the "Browse" button to be clickable and click it
    try:
        browse_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-action='pickFile']"))
        )
        browse_button.click()  # Click the Browse button to open the file dialog
    except Exception as e:
        print("Error waiting for the browse button to be clickable:", e)
        driver.quit()
        return

    # Step 3: Wait for the file input element to be ready and send the file path to it using pyautogui
    try:
        # Wait for the file dialog to open
        time.sleep(1)

        # Use pyautogui to type the file path into the file dialog
        print(f"Typing file path: {image_path}")
        pyautogui.typewrite(image_path)  # Type the file path
        pyautogui.press('enter')  # Press Enter to select the file

        # Give it a moment for the file to be uploaded
        time.sleep(3)
        
        if not switch_clicked:
            try:
                # Wait for and click the source language button
                src_lang_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='srcLangButton']"))
                )
                src_lang_button.click()
                # Wait for the element to be clickable and click it
                switch_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='langSelect']/div[1]/div[2]/div"))
                )
                switch_element.click()
                switch_clicked = True  # Set the flag to True after clicking
                
                # Wait for and click the Japanese language option
                japanese_option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='langSelect']/div[2]/div/div[24]"))
                )
                if japanese_option.get_attribute("aria-label") == "Japanese":
                    japanese_option.click()

                # Wait for and click the destination language button
                dst_lang_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='dstLangButton']"))
                )
                dst_lang_button.click()

                # Wait for and click the English language option
                english_option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='langSelect']/div[2]/div/div[24]"))
                )
                if english_option.get_attribute("aria-label") == "English":
                    english_option.click()

            except Exception as e:
                print(f"Error changing language: {e}")

    except Exception as e:
        print("Error interacting with the file dialog:", e)
        driver.quit()
        return

    # Step 4: Wait for the translated image to appear and capture its source URL
    try:
        # Wait for the download button to be clickable
        download_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='downloadButton']"))
        )
        # Click the download button
        download_button.click()

    except Exception as e:
        print(f"Error clicking download button: {e}")

    # Keep the driver open by not calling driver.quit() here.
    input("Press Enter to exit and close the browser...")

def change_language():
    #Change language
        try:
            # Wait for and click the source language button
            src_lang_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='srcLangButton']"))
            )
            src_lang_button.click()

            # Wait for and click the Japanese language option
            japanese_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='langSelect']/div[2]/div/div[24]"))
            )
            if japanese_option.get_attribute("aria-label") == "Japanese":
                japanese_option.click()

            # Wait for and click the destination language button
            dst_lang_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='dstLangButton']"))
            )
            dst_lang_button.click()

            # Wait for and click the English language option
            english_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='langSelect']/div[2]/div/div[24]"))
            )
            if english_option.get_attribute("aria-label") == "English":
                english_option.click()

        except Exception as e:
            print(f"Error interacting with language buttons: {e}")

def download_image():
    try:
        # Wait for the download button to be clickable
        download_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='downloadButton']"))
        )
        # Click the download button
        download_button.click()

    except Exception as e:
        print(f"Error clicking download button: {e}")

def close_tabs():
    # Close all other tabs except the current one
    current_window_handle = driver.current_window_handle
    all_window_handles = driver.window_handles
    for handle in all_window_handles:
        if handle != current_window_handle:
            driver.switch_to.window(handle)
            driver.close()
    driver.switch_to.window(current_window_handle) 

# GUI with a floating button (Tkinter)
def create_gui():
    root = tk.Tk()
    root.title("Floating Button App")
    root.geometry("200x100")

    # Create a floating button
    button = tk.Button(root, text="Capture Screenshot", command=capture_screenshot)
    button2 = tk.Button(root, text="Close Extra Tabs", command=close_tabs)
    button3 = tk.Button(root, text = "Change Language", command=change_language)
    button4 = tk.Button(root, text = "Download Image", command=download_image)
    button.pack(expand=True)
    button2.pack(expand=True)
    button3.pack(expand=True)
    button4.pack(expand=True)
    

    root.attributes("-topmost", True)  # Keep the window on top
    root.mainloop()

# Start both Selenium and Tkinter GUI
if __name__ == "__main__":
    create_gui()  # Run the GUI with the floating button
    # Clean up the driver when the GUI is closed
    if driver is not None:
        driver.quit()