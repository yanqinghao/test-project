from docx import Document


def get_text(filename):
    doc = Document(filename)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


print(get_text("private/雪浪-一步调用异常生成接口 V1.0(2).docx"))
