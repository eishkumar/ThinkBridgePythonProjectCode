import csv
import pandas as pd
import getpass
from playwright.async_api import async_playwright, Error


async def login(page):
    userName=input('Enter username and password for login \n#username: ')
    userPass=getpass.getpass('Enter Your Password:')
    await page.goto('https://www.linkedin.com/login')
    await page.fill('#username', userName)  # Replace with your LinkedIn username
    await page.fill('#password', userPass)  # Replace with your LinkedIn password
    await page.click('.login__form_action_container button')

# Function to Finf and get LinkedIn URLs for the companies
async def get_linkedin_url(companies):
    linkedin_urls = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context()

        for company in companies:
            try:
                page = await context.new_page()
                await page.goto(f'https://www.linkedin.com/company/{company}/')
                url = page.url
                if 'linkedin.com/company' in url:
                    linkedin_urls.append(url)
                else:
                    linkedin_urls.append('Not Found')
                await page.close()
            except Error as e:
                linkedin_urls.append('Not Found')

        await context.close()
        await browser.close()

    return linkedin_urls

# Function to get the employee count from LinkedIn for each company
async def get_employee_count(linkedin_urls):
    employee_counts = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await login(page)
        for url in linkedin_urls:
            try:
                page = await context.new_page()
                await page.goto(url)
                await page.wait_for_selector('a.org-top-card-summary-info-list__info-item span.link-without-visited-state')
                employee_count_element = await page.query_selector('a.org-top-card-summary-info-list__info-item span.link-without-visited-state')
                employee_count = await employee_count_element.inner_text()
                print(employee_count)
                emp_count=''.join(filter(str.isdigit, employee_count))
                employee_counts.append(emp_count)
                await page.close()
            except Error as e:
                employee_counts.append('Not Found')

        await context.close()
        await browser.close()

    return employee_counts

# Entry point function to process the CSV file and add LinkedIn URLs and employee counts
async def Run(csv_file):
    try:
        # Read CSV file and extract company names
        companies = []
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    companies.append(row[0].strip())

        # Find LinkedIn URLs for the companies
        linkedin_urls = await get_linkedin_url(companies)

        # Find employee counts from LinkedIn
        employee_counts = await get_employee_count(linkedin_urls)

        # Merge company names, LinkedIn URLs, and employee counts into a DataFrame
        data = {
            'Company': companies,
            'LinkedIn URL': linkedin_urls,
            'Employee Count': employee_counts
        }
        df = pd.DataFrame(data)
        # Save the DataFrame to a new CSV file
        output_file = csv_file
        print
        df.to_csv(output_file, index=False)

        return output_file

    except Exception as e:
        print(f"Error: {str(e)}")
        return None
