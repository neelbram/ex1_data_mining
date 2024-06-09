import json
import time
import os
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

URL = "https://www.indiegogo.com/explore/home?project=all&project=all&sort=trending"
NUM_ITEMS = 300


def scroll_main_page(driver):
    for i in range(NUM_ITEMS // 12):
        try:
            show_more_button = driver.find_element(
                By.XPATH, '//button[@gogo_test="show_more"]')
            if show_more_button:
                show_more_button.click()
                time.sleep(1)
        except Exception as e:
            driver.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)


def get_project_links(soup):
    project_links = []
    for a in soup.select('a[href*="/projects/"]'):
        href = a['href']
        if href.startswith('/projects/'):
            project_links.append(f"https://www.indiegogo.com{href}")
    return project_links


def scrape_project_data(driver, project_links):
    records = []
    for idx, project_url in enumerate(project_links[:NUM_OF_ITEMS], start=1):
        try:
            driver.get(project_url)
            driver.implicitly_wait(10)
            project = BeautifulSoup(driver.page_source, 'html.parser')

            title_div = project.find('div', class_='basicsSection-title')
            title = title_div.get_text(strip=True) if title_div else 'N/A'

            project_text_div = project.find(
                'div', class_='basicsSection-tagline')
            project_text = project_text_div.get_text(
                strip=True) if project_text_div else 'N/A'

            dollars_pledged_div = project.find(
                'div', class_='basicsGoalProgress-amountTowardsGoal')
            dollars_pledged_text = dollars_pledged_div.get_text(
                strip=True) if dollars_pledged_div else 'N/A'
            dollars_pledged = re.findall(
                r'\d+', dollars_pledged_text.replace(',', ''))
            dollars_pledged = dollars_pledged[0] if dollars_pledged else 'N/A'

            dollars_goal_div = project.find('span',
                                            class_='basicsGoalProgress-progressDetails-detailsGoal-goalPercentageOrInitiallyRaised')
            dollars_goal_text = dollars_goal_div.get_text(
                strip=True) if dollars_goal_div else 'N/A'
            dollars_goal_matches = re.findall(
                r'of ₪(\d+)', dollars_goal_text.replace(',', ''))
            dollars_goal = dollars_goal_matches[0] if dollars_goal_matches else 'N/A'

            num_backers_div = project.find(
                'span', class_='basicsGoalProgress-claimedOrBackers')
            num_backers_text = num_backers_div.get_text(
                strip=True) if num_backers_div else 'N/A'
            num_backers = re.findall(r'\d+', num_backers_text)
            num_backers = num_backers[0] if num_backers else 'N/A'

            days_to_go_div = project.find(
                'div', class_='basicsGoalProgress-progressDetails-detailsTimeLeft')
            days_to_go = re.findall(
                r'\d+', days_to_go_div.get_text(strip=True))[0] if days_to_go_div else 'InDemand'

            flexible_goal_div = project.find('span',
                                             class_='basicsGoalProgress-progressDetails-detailsGoal-goalPopover')
            flexible_goal = 'True' if flexible_goal_div and 'Flexible Goal' in flexible_goal_div.get_text(
                strip=True) else 'False'

            creators_div = project.find(
                'div', class_='basicsCampaignOwner-details-name')
            creators_text = creators_div.get_text() if creators_div else 'N/A'
            creators = creators_text.split('\n')[1].strip(
            ) if '\n' in creators_text else creators_text.strip()

            records.append({
                'id': str(idx),
                'url': project_url,
                'Creators': creators,
                'Title': title,
                'Text': project_text,
                'DollarsPledged': dollars_pledged,
                'DollarsGoal': dollars_goal,
                'NumBackers': num_backers,
                'DaysToGo': days_to_go,
                'FlexibleGoal': flexible_goal
            })
        except Exception as e:
            print(f"Error extracting project {project_url}: {e}")

    return records


def export_data(records, output_directory):
    data = {
        "records": {
            "record": records
        }
    }

    output_directory = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '..', 'output')
    os.makedirs(output_directory, exist_ok=True)
    output_path = os.path.join(output_directory, 'problem1.json')
    print("Output directory:", output_directory)
    print("Output file path:", output_path)
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    print("Exit Success")


def main():
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.implicitly_wait(10)

    scroll_main_page(driver)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    project_links = get_project_links(soup)

    records = scrape_project_data(driver, project_links)

    output_directory = 'output/problem1'

    export_data(records, output_directory)

    driver.quit()


main()
