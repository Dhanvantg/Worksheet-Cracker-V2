import openai
from PIL import Image, ImageFont, ImageDraw, ImageTk
from fpdf import FPDF
import random
import json
openai.api_key = "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"


def chatbot(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.0,
    )
    return response["choices"][0]["text"]


def punc(ques):
    if ques.endswith('?'):
        return ques
    else:
        return ques+'?'


def run(ques, cl):
    ques = ques.split('\n')
    lf = []
    for i in ques:

        lf.append(punc(i.replace('\r', '')))
    print(lf)
    print("Hi! I am Saul The Solver and I SAUL assignments!")
    idt = {"Name": "",
           "Suffix": "",
           "Type": "",
           "Page": ""}
    with open("Data/files/user.json", "w") as write_file:
        json.dump(idt, write_file)
    with open("Data/files/user.json") as rd:
        dat = json.load(rd)
    ast = "Data/assets/img"
    file1 = open("Data/files/answer.txt", "w")
    print("SAULING the assignment...")
    x = 1
    for q in lf:
        scl = chatbot(q)
        while scl.startswith('\n'):
            scl = scl[1:]
        file1.write(str(x) + "." + " " + q.capitalize() + "\n" + " " + scl + "\n\n")
        x += 1

    file1.close()
    print("Writing the assignment...")
    # Imposing on Image

    ar = file1 = open("Data/files/answer.txt", "r")
    text = ar.read()
    ar.close()
    img = Image.open("Data/assets/img/ruled1.png")
    base_width, base_height = img.size[0]-400, img.size[1]
    font = ImageFont.truetype("Danwriting.otf", 65)
    draw = ImageDraw.Draw(im=img)
    txt = text.split("\n")
    wd = 42
    ft = ""
    nl = 0
    for ln in txt:
        if len(ln) < wd:

            nl += 1
        elif len(ln) >= wd:
            wid = len(ln)
            nt = wid // wd
            it = 1
            while nt != 0:
                cp = wd*it
                rn = cp
                while ln[rn] != " ":
                    rn -= 1
                ln = ln[:rn]+"\n"+ln[rn:]
                nt -= 1
                it += 1
            nl += 1
        ft = ft+ln+"\n"
    ft = ft.split("\n")
    xs = 214
    xq = 140
    ys = 207
    yc = 58
    nl = 0
    np = 1
    pdl = []
    for fn in ft:
        try:
            if int(fn[:1]) > 0:
                ln = fn.replace(".", ".  ")
                draw.text(xy=(xq, ys + yc * nl), text=ln, font=font, fill='#000000')
        except:
            draw.text(xy=(xs, ys + yc * nl), text=fn, font=font, fill='#1961A3')
        nl+=1
        if nl >= 25:
            imp = "Output/pg" + str(np)
            img.save(imp + ".png")
            np += 1
            img = Image.open("Data/assets/img/ruled1.png")
            draw = ImageDraw.Draw(im=img)
            nl = 0
            pdl.append(imp+".png")
        else:
            imp = "Output/pg" + str(np)
            img.save(imp + ".png")
            if imp + ".png" not in pdl:
                pdl.append(imp + ".png")
    try:
        if pdl[0] == pdl[1]:
            pdl.pop(1)
    except:
        pass
    pdf = FPDF()
    # imagelist is the list with all image filenames
    shl = ["l1", "r1"]
    for image in pdl:
        shd = Image.open("Data/assets/img/"+random.choice(shl)+".png")
        img = Image.open(image).convert("RGBA")
        img.alpha_composite(shd)
        img.save(image)
        if cl == "BW":
            bw = Image.open(image).convert("LA")
            bw.save(image)
        pdf.add_page()
        pdf.set_auto_page_break(0)
        pdf.image(image, w = 200)
    pdf.output('Output/solved.pdf', "F")
    print(pdl)
    print("Successfully Created PDF")
    n = 0
    no = 1