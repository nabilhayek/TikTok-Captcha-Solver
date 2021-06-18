from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageDraw
import numpy as np

url = 'https://www.tiktok.com/'
browser = webdriver.Chrome()
browser.get(url)

try:
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "captcha-verify-image"))
    )
finally:
    captcha_element = browser.find_element_by_id("captcha-verify-image")
    captcha_element.screenshot('captcha.png')
    captcha_element.screenshot('ref.png')
    im = Image.open("captcha.png")
    cropped = im.crop((0, 50, 75, 200))
    cropped.save("template.png")
    
    data = np.array(cropped)

    red, green, blue, alpha = data.T
    white_areas = (red >= 215) & (blue >= 215) & (green >= 215)
    black_areas = (red < 215) | (blue < 215) | (green < 215)


    data[..., :-1][white_areas.T] = (255, 255, 255)
    data[..., :-1][black_areas.T] = (0, 0, 0)
    img = Image.fromarray(data.astype('uint8'))
    img.save('lol.png')

    draw = ImageDraw.Draw(im)
    draw.rectangle((5, 50, 75, 150), fill=(127, 127, 127), outline=(127, 127, 127))
    im.save('captcha.png')
    browser.quit()

