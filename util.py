def read_gzipped_json_from_url(url):
    # Send a HTTP request to the URL
    response = requests.get(url, verify=False)
    # Check if the request was successful
    if response.status_code == 200:
        # Use gzip to decompress the content
        with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as gz:
            # Read the JSON lines file and convert to a DataFrame
            df = pd.read_json(gz, lines=True)
        return df
    else:
        print(f"Failed to retrieve data: status code {response.status_code}")
        return None