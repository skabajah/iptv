import xml.etree.ElementTree as ET

# Input and output files
input_file = 'combined.xml'
output_file = 'cleaned.xml'

# Parse input XML
tree = ET.parse(input_file)
root = tree.getroot()

# Create a new root for cleaned XML
new_root = ET.Element('tv', attrib=root.attrib)

# Copy channel elements (only id and display-name)
for channel in root.findall('channel'):
    new_channel = ET.SubElement(new_root, 'channel', id=channel.get('id'))
    display_name = channel.find('display-name')
    if display_name is not None:
        new_display_name = ET.SubElement(new_channel, 'display-name')
        new_display_name.text = display_name.text

# Copy programme elements (only start, stop, channel, title)
for programme in root.findall('programme'):
    new_programme = ET.SubElement(new_root, 'programme', {
        'start': programme.get('start'),
        'stop': programme.get('stop'),
        'channel': programme.get('channel')
    })
    
    title = programme.find('title')
    if title is not None:
        new_title = ET.SubElement(new_programme, 'title')
        new_title.text = title.text

# Write cleaned XML to output file
cleaned_tree = ET.ElementTree(new_root)
cleaned_tree.write(output_file, encoding='utf-8', xml_declaration=True)
