import requests
import os
import io
import json
import time
import configparser


def main():

    # 1. Define raw directory, max length of the json message raw and the number of api units
    # 2. For each json file in the directory
    #   3. build single string of text
    #   4. make sure its within the size limit
    #   5. make sure we haven't hit our API limit
    #   6. send text array to the vendor
    #   7. create a results text file with the json and the text array
    #   8. throttle so we don't exceed our rate limit

    config = configparser.ConfigParser()
    config.read('config.ini')

    # 1. Define raw directory, max length of the json message raw and the number of api units
    data_dir_name = config['DEFAULT']['DATA_DIR_NAME']
    results_dir_name = config['DEFAULT']['RESULTS_DIR_NAME']
    max_length = int(config['IDL']['IDL_MAX_LENGTH'])
    api_units_left = int(config['IDL']['IDL_API_UNITS_LEFT'])  # the starting number of units every day
    max_requests_per_min = int(config['DEFAULT']['MAX_REQUESTS_PER_MIN'])
    idl_api_key = config['IDL']['IDL_API_KEY']

    # walk the directory
    for root_dir_name, subdir_list, file_list in os.walk(data_dir_name):
        base_dir_name = os.path.basename(root_dir_name)
        if base_dir_name == data_dir_name:
            continue

        print('Processing directory: %s' % base_dir_name)
        processed_file_count = 1
        file_count = len(file_list)

        # 2. For each json file in the directory
        for filename in file_list:
            print('Processing {}/{}'.format(processed_file_count, file_count))
            processed_file_count += 1
            if filename.endswith(('.json')):
                filepath = os.path.join(data_dir_name, filename)

                # 3. build single string of text
                text = build_text(filepath)

                # 4. make sure its within the size limit
                truncated_text = truncate_text_to_limit(filepath, text, max_length)

                # 5. make sure we haven't hit our API limit
                if api_units_left <= 0:
                    print('API Units exhausted.')
                    exit(1)

                # 6. send text array to the vendor
                results = send_text_to_idl(idl_api_key, filepath, truncated_text)

                api_units_left = results.json()['request']['units_left']
                if results.status_code != requests.codes.ok:
                    print('Error processing: {}'.format(filepath))
                    print('Error: {}'.format(results.json()))
                else:
                    # 7. create a results text file with the json and the text array
                    write_results_to_file(results_dir_name, filename, results.json(), text)

                    check_for_significant_interests(filename, results.json()['response'][0]['interests'])

                    # 8. throttle so we don't exceed our rate limit
                    time.sleep(60 / max_requests_per_min)


def build_text_list(filepath):
    text_list = []
    with open(filepath, 'r') as f:
        datastore = json.load(f)
        for message_item in datastore:
            text_list.append(message_item['message'])
    return text_list


def build_text(filepath):
    text = ''
    with open(filepath, 'r') as f:
        datastore = json.load(f)
        for message_item in datastore:
            text += message_item['message']
    return text


def truncate_text_to_limit(filepath, text, max_length):
    if utf8len(text) > max_length:
        print("Truncating: {}".format(filepath))
        text = text[:max_length]
    return text


def utf8len(s):
    return len(s.encode('utf-8'))


def send_text_to_idl(idl_api_key, filepath, text):
    payload = {'apikey': idl_api_key, 'models': 'interests'}
    data = {'texts': [text]}
    r = requests.post('https://api.indatalabs.com/v1/text', params=payload, json=data)
    return r


def write_results_to_file(results_dir_name, filename, result_json, text):
    result_filepath = results_dir_name + '/' + filename + '.results.txt'
    with io.open(result_filepath, 'w+', encoding='UTF-8') as f:
        f.write('API RESPONSE:\n')
        json.dump(result_json, f, sort_keys=True, indent=4, ensure_ascii=False)
        f.write('\nMESSAGE CONTENT:\n')
        f.write(text)


def check_for_significant_interests(filename, interests):
    significant_interests = []
    for k, v in interests.items():
        if v >= 1.0:
            significant_interests.append([k, v])
    if len(significant_interests) > 0:
        print('{} has significant interests: {}'.format(filename, significant_interests))


def test_call_to_idl(idl_api_key):
    # make a call to:
    # https://api.indatalabs.com/v1/text

    payload = {'apikey': idl_api_key, 'models': 'interests'}
    data = {
        "texts": [
            "Regardless of the industry, Data Science and Artificial Intelligence promise to reshape the way we do our jobs every day. At InData Labs we seek to bring the power of raw science & AI to our customers.",
            "Whether you want to explore the possible use cases for big raw analytics or have an AI solution in mind and want to start quickly, our team of world-class raw scientists and raw engineers can help you achieve big raw success and get the most out of your investment."
        ]
    }
    r = requests.post('https://api.indatalabs.com/v1/text', params=payload, json=data)

    print(r.url)
    print(r.json())


if __name__ == '__main__':
    main()
