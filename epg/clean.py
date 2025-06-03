import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

# Files
tvg_id_file = 'tvg-id'
input_xml = 'combined.xml'
output_xml = 'cleaned.xml'

# Read channel IDs from tvg-id file
with open(tvg_id_file, 'r', encoding='utf-8') as file:
    channels_to_keep = [
        line.strip() for line in file
        if line.strip() and line.strip() != '(no tvg-id)' and line.strip() != 'tvg-id'
    ]

# Parse input XML
tree = ET.parse(input_xml)
root = tree.getroot()

# New filtered root
new_root = ET.Element('tv', attrib=root.attrib)

# Filter channels
for channel in root.findall('channel'):
    channel_id = channel.get('id')
    if channel_id in channels_to_keep:
        new_channel = ET.SubElement(new_root, 'channel', id=channel_id)
        display_name = channel.find('display-name')
        if display_name is not None:
            ET.SubElement(new_channel, 'display-name').text = display_name.text

# Filter programmes
for programme in root.findall('programme'):
    if programme.get('channel') in channels_to_keep:
        new_programme = ET.SubElement(new_root, 'programme', {
            'start': programme.get('start'),
            'stop': programme.get('stop'),
            'channel': programme.get('channel')
        })
        title = programme.find('title')
        if title is not None:
            ET.SubElement(new_programme, 'title').text = title.text

# Pretty print and save XML
xml_str = ET.tostring(new_root, encoding='utf-8')
pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")

with open(output_xml, "w", encoding="utf-8") as f:
    f.write(pretty_xml)

print(f"Filtered XML written to {output_xml}")
