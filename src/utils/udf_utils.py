import re


def fix_response_text(text):
    removed_irrelevant_text = re.sub('exports.Battle.*?= ', '',
                                     text.replace("'", '').replace('â\x80\x99d', '')
                                     .replace(';', '')
                                     .replace('Ì\x81beÌ\x81', 'be')
                                     .replace('Type: Null', 'Type Null'))
    json_string = re.sub(',desc:.*?"}', '}', removed_irrelevant_text)
    return re.sub("(\w+):", r'"\1":', json_string)
