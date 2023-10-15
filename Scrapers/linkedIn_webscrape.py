import requests
from bs4 import BeautifulSoup

def scrape_profiles(keyword):
    # Set up the base URL and headers
    base_url = 'https://www.linkedin.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Log in to LinkedIn
    session = requests.Session()
    login_url = f'{base_url}/login'
    login_response = session.get(login_url, headers=headers)
    login_soup = BeautifulSoup(login_response.content, 'html.parser')
    csrf_token = login_soup.find('input', {'name': 'loginCsrfParam'}).get('value')
    payload = {
        'session_key': 'thjobjabber@gmail.com',
        'session_password': 'Th67237837!##1',
        'loginCsrfParam': csrf_token,
    }
    session.post(login_url, headers=headers, data=payload)

    # Search for profiles with the given keyword
    profiles = []
    for page in range(1, 21):
        search_url = f'{base_url}/search/results/people/?keywords={keyword}&page={page}'
        search_response = session.get(search_url, headers=headers)
        search_soup = BeautifulSoup(search_response.content, 'html.parser')

        # Get the URLs of the matching profiles
        for link in search_soup.find_all('a', {'class': 'app-aware-link'}):
            url = link.get('href')
            if '/in/' in url:
                profiles.append(url)

    # Scrape profile information
    profile_data = []
    for profile in profiles:
        profile_url = f'{base_url}{profile}'
        profile_response = session.get(profile_url, headers=headers)
        profile_soup = BeautifulSoup(profile_response.content, 'html.parser')

        # Find the profile description/experience section and search for the keyword
        experience_section = profile_soup.find('section', {'id': 'experience-section'})
        if experience_section:
            for experience in experience_section.find_all('div', {'class': 'pv-entity__summary-info'}):
                if keyword in str(experience).lower():
                    profile_data.append({
                        'Name': profile_soup.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).text.strip(),
                        'Job Title': experience.find('h3', {'class': 't-16 t-black t-bold'}).text.strip(),
                        'Company': experience.find('p', {'class': 'pv-entity__secondary-title t-14 t-black t-normal'}).text.strip(),
                        'Keyword': keyword
                    })

    return profile_data

if __name__ == '__main__':
    keyword = 'customer'
    profiles = scrape_profiles(keyword)
    print(f'Found {len(profiles)} profiles with the keyword "{keyword}"')
    print(profiles)
