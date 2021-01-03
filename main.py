import pandas as pd
import sys
import re
import math
"""
image alt text scheme
Kindermode Kurze Hose Anzugsshorts Jungs Dunkelblau GlowingKids Shorts Front
(Kindermode) (Produktname) (Gender) (Produktfarbe) (GlowingKids) (Keyword1)(Ansicht)
handle scheme
(Kindermode)-(Produktname)-(Gender)-(Produktfarbe)
SEO title scheme 
{Produktname} {|} {GlowingKids Kindermode}
SEO description scheme
{GlowingKids steht für qualitativ hochwertige Kindermode. Die Kollektionen werden liebevoll im 
skandinavischen und belgischen Stil zusammengestellt. ✓hochwertige Mode ✓schneller Versand ✓sichere Bezahlung} 
"""
def main(argv):
    data = pd.read_csv(argv[1], sep=',', encoding='utf-8')
    data.columns = data.columns.map(lambda x: x.replace(' ', '_'))
    # get only those rows with images
    data_filtered = data.loc[:, :'Gift_Card']
    data_filtered = data_filtered[(~data_filtered['Image_Src'].isnull())]
    data.loc[:, 'SEO_Description'] = 'GlowingKids steht für qualitativ hochwertige Kindermode. Die Kollektionen werden ' \
                                  'liebevoll im skandinavischen und belgischen Stil zusammengestellt. ' \
                                  '✓hochwertige Mode ✓schneller Versand ✓sichere Bezahlung'
    prev = ''
    alt_text = ''
    handle_occur={}
    for row in data_filtered.itertuples():
        handle = row[1]
        image_pos = row[25]
        if image_pos == 1:
            image_pos = 'Front'
        elif image_pos == 2:
            image_pos = 'Back'
        elif image_pos == 3:
            image_pos = 'Left'
        else:
            image_pos = 'Right'
        if prev == row[1]:
            alt_text = alt_text.rsplit(' ', 1)[0] + ' ' + image_pos
            print(alt_text)
            # use index (row[0]) to update only specific rows which have images
            data.loc[row[0],'Image_Alt_Text'] = alt_text
            continue
        print(row[1])
        if row[1] == 'geschenkgutschein':
            data.loc[row[0], 'Image_Alt_Text'] = 'Kindermode ' + row[2] + ' GlowingKids ' + image_pos
            #handle = 'Kindermode ' + row[2] + ' Glowing Kids'
            #handle = handle.lower().replace(' ','-')
            #data.loc[data['Handle'] == row[1], 'Handle'] = handle
            data.loc[data['Handle'] == handle, 'SEO_Title'] = row[2] + ' | GlowingKids Kindermode'
            continue
        gender = re.findall(r'Gender_\w+', row[6])[0].split('_')[1]
        try:
            keyword_1 = re.findall(r'Keyword1_\w+', row[6])[0].split('_')[1] + ' '
        except Exception as e:  # in case there is no keyword1
            pass
            keyword_1 = ''

        color = row[11]
        if row[1] == 'rosa-tasche':
            color = row[9]
        if type(color) != str and math.isnan(row[11]):
            color = ''
        alt_text = 'Kindermode ' + row[2] + ' ' + gender + ' ' + color + ' GlowingKids ' + keyword_1 + image_pos
        #handle = 'Kindermode-' + row[2] + '-' + gender + '-' + color
        #if color == '':
        #    handle = handle.rstrip('-')
        #handle = handle.lower().replace(' ', '-').replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe').replace('ß', 'ss').replace('é', 'e')
        seo_title = row[2] +' | GlowingKids Kindermode'
        #print(alt_text)
        # use index (row[0]) to update only specific rows which have images
        data.loc[row[0],'Image_Alt_Text'] = alt_text

        data.loc[data['Handle'] == handle, 'SEO_Title'] = seo_title
        '''if handle not in handle_occur.keys():
            handle_occur[handle] = 0
            data.loc[data['Handle'] == row[1], 'Handle'] = handle
        else:
            handle_occur[handle] = handle_occur[handle] + 1
            handle += '-' + str(handle_occur[handle])
            data.loc[data['Handle'] == row[1], 'Handle'] = handle'''
        prev = row[1]
    #print(data['Image_Alt_Text'])
    #print(data['SEO_Title'])
    print(handle_occur)
    data.columns = data.columns.map(lambda x: x.replace('_', ' '))
    data.to_csv('p_e2.csv', sep=',', encoding='utf-8', index=False)


if __name__ == "__main__":
    main(sys.argv)