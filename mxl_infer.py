from lxml import etree

note_template = """
<note default-x="155.23" default-y="-45.00">
<pitch>
  <step>{step}</step>
  <octave>{octave}</octave>
  </pitch>
<duration>4</duration>
<voice>1</voice>
<type>{type}</type>
<stem>up</stem>
<lyric default-x="6.58" default-y="-45.34" relative-y="-30.00">
  <syllabic>single</syllabic>
  <text>{lyric}</text>
</lyric>
</note>
"""


barline_template = """
<barline location="right">
<bar-style>light-light</bar-style>
</barline>
"""

rest_template = """
<note>
<rest/>
<duration>4</duration>
<voice>1</voice>
<type>eighth</type>
</note>
"""


measure_start_template = """
<measure number="{number}">
"""

measure_end_template = """
</measure>
"""


def read_file(file_name):
    with open(file_name, 'r') as f:
        return [i.strip() for i in f]


def write_file(file_name, data):
    with open(file_name, 'w') as f:
        for i in data:
            f.write(i + '\n')
        f.close()


def format_xml(template_name, output_file, notes):
    with open(template_name, 'r') as f:
        xml = f.read()
        xml = bytes(bytearray(xml, encoding='utf-8'))
        root = etree.XML(xml)
        for part in root.findall('part'):
            # for measure in part.findall('measure'):
            # for note in notes:
                # measure.append(etree.fromstring(note))
            # print(' '.join(notes))
            # print(etree.fromstring(notes[0]))
            # part.append(etree.fromstring(notes[0] + notes[1]))
            for measure in notes:
                part.append(etree.fromstring(measure))

        tree = etree.ElementTree(root)
        tree.write(output_file + '.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")


def format_note(lyric, note_features, template):
    step, octave, type = note_features.split('_')
    res = template.format(step=step.upper(), octave=octave, type=type, lyric=lyric)
    return res


def save_as_mxl(predicted_notes):
    xml_notes = []
    counter = 1
    for notes in predicted_notes:
        mes_start = measure_start_template.format(number=counter)
        notes = notes[:-1]
        # print(words, notes)
        # for lyric, note in zip(words, notes):
        #     xml_notes.append(format_note(lyric, note, note_template))
        #     mes_start += format_note(lyric, note, note_template)
        for note in notes:
            mes_start += format_note('lyric', note, note_template)
        mes_start += rest_template
        mes_start += measure_end_template
        # xml_notes.append(measure_end_template)
        xml_notes.append(mes_start)
        counter += 1
    print(xml_notes)
    format_xml('template.xml', 'infer', xml_notes)
    # write_file(file_name.split('.')[0]+'.notes', predicted_notes)

