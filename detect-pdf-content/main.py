import os
import argparse
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject, NameObject

import detect_pdf_lines, word_spacing


def replace_text(content, transformed_input_output):
    lines = content.splitlines()

    result = ""
    in_text = False
    for line in lines:
        if line == "BT":
            in_text = True

        elif line == "ET":
            in_text = False

        elif in_text:
            # Test the function with your input
            # input_string = "/F28 9.9626 Tf 166.174 707.125 Td [(Lorem)-333(ipsum)-334(dolor)-333(sit)-333(amet,)-334(consectetuer)-333(adipiscing)-333(elit.)-445(Ut)-333(purus)-333(elit,)]TJ -19.4 -11.955 Td [(v)28(estibulum)-334(ut)1(,)-334(placerat)-333(ac,)-334(ad)1(ipiscing)-334(vitae,)-333(felis.)-445(Cu)1(rabitur)-334(dictum)-333(gra)28(vida)]TJ -12.121 -11.955 Td [(mauris.)-444(Nam)-334(arcu)-333(lib)-28(ero,)-333(non)28(umm)27(y)-333(eget,)-333(consectetuer)-334(id,)-333(vulputate)-333(a,)-334(magna.)]TJ -0.885 -11.955 Td [(Donec)-317(v)28(ehicula)-317(augue)-316(eu)-317(neque.)-439(P)28(ellen)28(tesque)-317(habitan)28(t)-317(morbi)-316(tristique)-317(senectus)]TJ 18.514 -11.956 Td [(et)-333(netus)-334(et)-333(malesuada)-333(fames)-334(ac)-333(turpis)-333(e)-1(gestas.)-444(Mauris)-333(ut)-334(leo.)-444(Cras)-333(viv)27(erra)]TJ 22.554 -11.955 Td [(metus)-333(rhoncus)-334(sem.)-444(Nulla)-334(et)-333(lectus)-333(v)28(e)-1(stib)1(ulum)-334(urna)-333(fringilla)-333(ultrices.)]TJ -36.198 -11.955 Td [(Phasellus)-333(eu)-334(tellus)-333(sit)-333(amet)-334(tortor)-333(gra)28(vida)-334(p)1(lace)-1(rat.)-444(In)28(teger)-334(sapi)1(e)-1(n)-333(est,)-333(iaculis)]TJ 41.678 -11.955 Td [(in,)-333(pretium)-333(quis,)-334(viv)28(erra)-333(ac,)-334(n)28(unc.)-444(Praesen)28(t)-334(eget)-333(sem)-334(v)28(el)-333(leo)-334(ultr)1(ice)-1(s)]TJ -30.691 -11.955 Td [(bib)-28(endum.)-444(Aenean)-333(faucibus.)-445(Morbi)-333(dolor)-333(n)28(ulla,)-334(malesuada)-333(eu,)-333(pulvinar)-333(at,)]TJ -7.887 -11.955 Td [(mollis)-333(ac,)-334(n)28(ulla.)-444(Curabitur)-333(auctor)-334(semp)-28(er)-333(n)28(ulla.)-444(Donec)-334(v)56(arius)-334(orci)-333(eget)-333(risus.)]TJ -7.97 -11.956 Td [(Duis)-333(ni)1(bh)-333(mi,)-333(congue)-332(eu,)-333(accumsan)-333(eleifend)1(,)-333(sagittis)-333(quis,)-332(diam.)-445(Du)1(is)-333(eget)-333(orci)]TJ 207.859 -11.955 Td [(sit)-333(amet)-334(orci)-333(dignissim)-333(rutrum.)]TJ -207.859 -21.918 Td [(Nam)-315(dui)-315(ligula,)-318(fringilla)-315(a,)-319(euismo)-28(d)-315(so)-27(dales,)-319(sollicitudin)-315(v)28(el,)-319(wisi.)-438(Morbi)-315(auctor)]TJ 23.163 -11.955 Td [(lorem)-333(non)-334(justo.)-444(Nam)-333(lacus)-334(lib)-27(ero,)-334(pretium)-333(at,)-333(lob)-28(ortis)-333(vitae,)-334(ultricies)-333(et,)]TJ 5.784 -11.955 Td [(tellus.)-444(Donec)-334(aliquet,)-333(tortor)-333(sed)-334(accumsan)-333(bib)-28(endum,)-333(erat)-333(ligula)-334(aliquet)]TJ -16.826 -11.955 Td [(magna,)-333(vitae)-334(ornare)-333(o)-28(dio)-333(metus)-333(a)-334(mi.)-444(Morbi)-333(ac)-334(orci)-333(et)-333(nisl)-334(hendrerit)-333(mollis.)]TJ 22.914 -11.955 Td [(Susp)-28(endisse)-333(ut)-333(mas)-1(sa.)-444(Cras)-333(nec)-334(an)28(te.)-444(P)27(ellen)28(tesque)-333(a)-334(n)28(ulla.)-444(Cum)-333(so)-28(ciis)]TJ -21.143 -11.955 Td [(nato)-28(que)-333(p)-28(enatibus)-333(et)-333(magnis)-334(dis)-333(parturien)28(t)-334(mon)28(tes,)-333(nascetur)-333(ridiculus)-334(m)28(us.)]TJ 0.083 -11.956 Td [(Aliquam)-333(tincidun)28(t)-334(urna.)-444(Nulla)-333(ullamcorp)-28(er)-333(v)27(estibu)1(lum)-334(turpis.)-444(P)28(ellen)27(tesque)]TJ 237.582 -11.955 Td [(cursus)-333(luctus)-334(mauris.)]TJ -234.178 -21.918 Td [(Nulla)-333(malesuada)-334(p)-27(orttitor)-334(diam.)-444(Donec)-333(felis)-334(erat,)-333(congue)-333(non,)-334(v)28(olutpat)-333(at,)]TJ -12.841 -11.955 Td [(tincidun)28(t)-333(tristique,)-334(lib)-27(ero.)-445(Viv)56(am)28(us)-334(viv)28(erra)-333(fermen)27(tu)1(m)-334(felis.)-444(Donec)-334(non)28(umm)28(y)]TJ -4.538 -11.955 Td [(p)-28(ellen)28(tesque)-327(an)28(te.)-443(Phasellus)-327(adipiscing)-327(semp)-28(er)-327(elit.)-442(Proin)-328(f)1(e)-1(r)1(m)-1(en)28(tum)-327(massa)-327(ac)]TJ 1.107 -11.955 Td [(quam.)-444(Sed)-334(diam)-333(turpis,)-333(molestie)-334(vitae,)-333(placerat)-333(a,)-334(molestie)-333(nec,)-333(leo.)-445(Maecenas)]TJ -0.028 -11.955 Td [(lacinia.)-444(Nam)-334(ipsum)-333(ligula,)-333(eleifend)-334(at,)-333(accumsan)-333(nec,)-334(suscipit)-333(a,)-333(ipsum.)-445(Morbi)]TJ 0.221 -11.956 Td [(blandit)-333(ligula)-333(feugiat)-334(magna.)-444(Nunc)-333(ele)-1(i)1(fend)-334(consequat)-333(lorem.)-445(Sed)-333(lacinia)-333(n)28(ulla)]TJ 33.541 -11.955 Td [(vitae)-333(enim.)-445(P)28(ellen)28(tesque)-334(tincidun)28(t)-333(purus)-333(v)28(el)-334(magna.)-444(In)28(tege)-1(r)-333(non)-333(enim.)]TJ -18.514 -11.955 Td [(Praesen)28(t)-334(euismo)-27(d)-334(n)28(unc)-333(eu)-334(pu)1(rus.)-445(Donec)-333(bib)-28(endum)-333(quam)-334(in)-333(tellus.)-444(Nullam)]TJ 29.196 -11.955 Td [(cursus)-333(pulvinar)-334(lectus.)-444(Donec)-333(et)-334(mi.)-444(Nam)-334(vulp)1(utate)-334(metus)-333(eu)-334(enim.)]TJ 126.886 -11.955 Td [(V)83(estibulum)-333(p)-28(ellen)28(tesque)-333(felis)-334(eu)-333(massa.)]TJ -159.818 -21.918 Td [(Quisque)-333(ullamcorp)-28(er)-333(placerat)-334(ipsum.)-444(Cras)-333(nibh.)-445(Morbi)-333(v)28(el)-334(ju)1(s)-1(to)-333(vitae)-333(lacus)]TJ -12.01 -11.955 Td [(tincidun)28(t)-333(ultrices.)-445(Lorem)-333(ipsum)-334(d)1(olor)-334(sit)-333(amet,)-334(consectetuer)-333(adipiscing)-333(elit.)-445(In)]TJ 0.802 -11.955 Td [(hac)-333(habitasse)-334(platea)-333(dictumst.)-444(I)-1(n)28(teger)-333(tempus)-333(con)27(v)56(allis)-333(augue.)-445(Etiam)-333(facilisis.)]TJ 12.537 -11.956 Td [(Nunc)-333(elemen)27(tum)-333(fermen)28(tum)-333(w)-1(i)1(s)-1(i.)-444(Aenean)-333(placerat.)-445(Ut)-333(imp)-28(erdiet,)-333(enim)-333(s)-1(ed)]TJ -11.983 -11.955 Td [(gra)28(vida)-333(sollicitudin,)-334(felis)-333(o)-28(dio)-333(placerat)-333(quam,)-334(ac)-333(pulvinar)-333(elit)-333(purus)-334(eget)-333(enim.)]TJ 0.553 -11.955 Td [(Nunc)-333(vitae)-334(tortor.)-444(Proin)-333(tempus)-334(nib)1(h)-334(sit)-333(amet)-334(ni)1(s)-1(l.)-444(Viv)56(am)27(us)-333(quis)-333(tortor)-334(vi)1(tae)]TJ 252.775 -11.955 Td [(risus)-333(p)-28(orta)-333(v)27(ehicula.)]TJ -85.9 -107.597 Td [(1)]TJ"
            # input_string = "/F39 20.6625 Tf 126.285 1033.335 Td [(1)-1125(Assignmen)31(t)-375(2.5)]TJ/F39 17.2154 Tf 0 -36.125 Td [(1.1)-1125(Exercises)-375(1)]TJ/F37 14.3462 Tf 0 -26.202 Td [(Consider)-480(the)-327(pro)1(gram)]TJ/F42 14.3462 Tf 138.988 0 Td [(C)]TJ/F37 14.3462 Tf 15.763 0 Td [(and)-326(pre-)-327(and)-326(p)-27(ostconditions)]TJ/F42 14.3462 Tf 176.916 0 Td [(F)]TJ/F37 14.3462 Tf 15.727 0 Td [(and)]TJ/F42 14.3462 Tf 27.314 0 Td [(H)]TJ/F37 14.3462 Tf 17.429 0 Td [(as)-326(follo)27(ws:)]TJ"
            transformed_input = word_spacing.transform_input(line)
            transformed_input_output.extend(transformed_input)
        result += line + "\n"
    
   
    return result


def process_data(object, replacements):
    data = object.get_data()
    decoded_data = data.decode()

    replaced_data = replace_text(decoded_data, replacements)
    encoded_data = replaced_data.encode()
    if object.decoded_self is not None:
        object.decoded_self.set_data(encoded_data)
    else:
        object.set_data(encoded_data)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="path to PDF document")
    args = vars(ap.parse_args())

    in_file = args["input"]
    filename_base = in_file.replace(os.path.splitext(in_file)[1], "")

    # Provide replacements list that you need here
    transformed_input_output =  []


    reader = PdfReader(in_file)
    writer = PdfWriter()

    for page_number in range(0, len(reader.pages)):

        page = reader.pages[page_number]
        contents = page.get_contents()

        if isinstance(contents, DecodedStreamObject) or isinstance(contents, EncodedStreamObject):
            process_data(contents, transformed_input_output)
        elif len(contents) > 0:
            for obj in contents:
                if isinstance(obj, DecodedStreamObject) or isinstance(obj, EncodedStreamObject):
                    streamObj = obj.get_object()
                    process_data(streamObj, transformed_input_output)

        
        page[NameObject("/Contents")] = contents.decoded_self
        writer.add_page(page)
    
    word_spacing.write_array_to_file(transformed_input_output,'transformed-output.txt')
    output = detect_pdf_lines.detectPdfLines(transformed_input_output)
    word_spacing.write_array_to_file(output,'output.txt')

    with open(filename_base + ".result.pdf", 'wb') as out_file:
        writer.write(out_file)