def modified_pdf_lines(pdf_lines):
    updated_pdf_lines = []
    for item in pdf_lines:
        content_adjustment = item['line-adjustment']
        content_text = item['content']
        if isinstance(content_adjustment, list):
            for item in content_adjustment:
                updated_pdf_lines.append(item)
        else:
            updated_pdf_lines.append(content_adjustment)

        if content_text and isinstance(content_text,list):
            for item in content_text:
                updated_pdf_lines.append(item)
    return updated_pdf_lines
        

            
                

