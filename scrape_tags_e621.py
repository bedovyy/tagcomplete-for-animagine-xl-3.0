import os
import requests
import collections
import csv
import time

csv_filename = input('Output filename: ')
minimum_count = input('Minimum tag count (> 50 is preferable): ')
dashes = input('replace \'_\' with \'-\'? (often better for prompt following) (Y/n): ')
exclude = input('enter categories to exclude: (general,artist,copyright,character,post) (press enter for none): \n')
alias = input('Include aliases? (Only supported in tag-complete) (y/N): ')

excluded = ""
excluded += "0" if "general" in exclude else ""
excluded += "1" if "artist" in exclude else ""
excluded += "3" if "copyright" in exclude else ""
excluded += "4" if "character" in exclude else ""
excluded += "5" if "post" in exclude else ""

kaomojis = [
    "0_0", "(o)_(o)", "+_+", "+_-", "._.", "<o>_<o>", "<|>_<|>", "=_=", ">_<",
    "3_3", "6_9", ">_o", "@_@", "^_^", "o_o", "u_u", "x_x", "|_|", "||_||",
]

if not '.csv' in csv_filename:
    csv_filename += '.csv'

if not 'n' in dashes.lower():
    dashes = 'y'
    csv_filename += '-temp'

if not 'y' in alias.lower():
    alias = 'n'

if not minimum_count.isdigit():
    minimum_count = 50

# Base URL without the page parameter
base_url = 'https://e621.net/tags.json?limit=320&search[hide_empty]=yes&search[order]=count'
alias_url = 'https://e621.net/tag_aliases.json?limit=320&search[order]=tag_count'

aliases = {}

aliases = collections.defaultdict(str)

headers = { "User-Agent": "collecting_tags/1.0" }

if alias == 'y':
    # create alias dictionary
    for page in range(1,751):
        # Update the URL with the current page
        url = f'{alias_url}&page={page}'
        # Fetch the JSON data
        response = requests.get(url, headers=headers)
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Break the loop if the data is empty (no more tags to fetch)
            if not data or (len(data) == 1 and 'tag_aliases' in data):
                print(f'No more data found at page {page}. Stopping.', flush=True)
                break
            for item in data:
                aliases[item['consequent_name']] += ',' + item['antecedent_name'] if aliases[item['consequent_name']] else item['antecedent_name']
        else:
            print(f'Failed to fetch data for alias page {page}. HTTP Status Code: {response.status_code}', flush=True)
            break
        print(f'Page {page} aliases processed.', flush=True)
        # Sleep for 0.5 second because we have places to be
        time.sleep(0.5)

# Open a file to write
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Loop through pages 1 to 750
    class Complete(Exception): pass
    try:
        for page in range(1, 751):
            # Update the URL with the current page
            url = f'{base_url}&page={page}'

            # Fetch the JSON data
            response = requests.get(url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()

                # Break the loop if the data is empty (no more tags to fetch)
                if not data or (len(data) == 1 and 'tags' in data):
                    print(f'No more data found at page {page}. Stopping.', flush=True)
                    break
                
                # Write the data
                for item in data:
                    if int(item['post_count']) < int(minimum_count): # break if below minimum count
                        file.flush()
                        raise Complete
                    if not str(item['category']) in excluded:
                        if alias == 'n':
                            writer.writerow([item['name'],item['category'],item['post_count'],''])
                        else:
                            alt = aliases.get(item['name']) if aliases.get(item['name']) != None else ''
                            writer.writerow([item['name'],item['category'],item['post_count'],alt])

                # Explicitly flush the data to the file
                file.flush()
            else:
                print(f'Failed to fetch data for page {page}. HTTP Status Code: {response.status_code}', flush=True)
                break

            print(f'Page {page} processed.', flush=True)
            # Sleep for 0.5 second because we have places to be
            time.sleep(0.5)
    except Complete:
        print(f'All tags with {minimum_count} posts or greater have been scraped.')
    file.close()

    if dashes == 'y':
        print(f'Replacing \'_\' with \'-\'')
        with open(csv_filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            with open(csv_filename.removesuffix('-temp'), 'w', encoding='utf-8', newline='') as outfile:
                writer = csv.writer(outfile)
                for row in reader:
                    if not row[0] in kaomojis:
                        row[0] = row[0].replace("_", "-")
                        row[3] = row[3].replace("_", "-")
                    writer.writerow(row)
                outfile.close()    
            csvfile.close()
        os.remove(csv_filename)
        csv_filename = csv_filename.removesuffix('-temp')

print(f'Data has been written to {csv_filename}', flush=True)
