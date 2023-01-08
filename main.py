import openai
from PIL import Image, ImageFont, ImageDraw
from fpdf import FPDF
import random

openai.api_key = "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"
pdl = []

def chatbot(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.0,
    )
    return response["choices"][0]["text"]


def punc(ques):
    if ques[-1] in ('?.!'):
        return ques
    else:
        return ques + '?'


def run(ques, cl, uname, hwrite, app):

    def draw(txt, clr, hwrite, line, page, uname, img):
        if hwrite == '1':
            ys = 207
            font = ImageFont.truetype("static/fonts/Danwriting.otf", 65)
        else:
            ys = 236
            font = ImageFont.truetype("static/fonts/JustMeAgainDownHere-Regular.ttf", 60)
        draw = ImageDraw.Draw(im=img)
        txt = txt.split("\n")
        wd = 43
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
                    cp = wd * it
                    rn = cp
                    while ln[rn] != " ":
                        rn -= 1
                    ln = ln[:rn] + "\n" + ln[rn:]
                    nt -= 1
                    it += 1
                nl += 1
            ft = ft + ln + "\n"
        ft = ft.split("\n")
        xs = 214
        xq = 150
        yc = 58
        nl = line
        np = page
        cnt = 0
        nos = 0
        for fn in ft:
            if clr:
                colr = '#1961A3'
                fn = '   ' + fn
            else:
                colr = '#000000'
                fn = fn.replace(".", ".  ")
                if nos > 0:
                    fn = '   ' + fn
                nos += 1
            draw.text(xy=(xq, ys + yc * nl), text=fn, font=font, fill=colr)
            cnt += 1
            nl += 1
            if nl >= 25:
                imp = "Output/" + uname + str(np)
                img.save(imp + ".png")
                np += 1
                print(uname, page)
                nl = 0
                if imp + ".png" not in pdl:
                    pdl.append(imp + ".png")
                return nl, pdl, np, Image.open("Data/assets/img/ruled1.png")
            else:
                imp = "Output/" + uname + str(np)
                img.save(imp + ".png")
                if imp + ".png" not in pdl:
                    pdl.append(imp + ".png")
        return nl, pdl, np, Image.open("Output/"+uname+str(page)+".png")

    if app == 1:
        ques = ques.split('\n')
        lf = []
        for i in ques:
            lf.append(punc(i.replace('\r', '')))
        print(lf)
        print("Hi! I am Saul The Solver and I SAUL assignments!")
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

    else:
        file1 = open("Data/files/answer.txt", "w")
        file1.write(ques)
        file1.close()
    ar = open("Data/files/answer.txt", "r")
    text = ar.read()
    text = text.replace('\n\n', '\n')
    ar.close()
    print("Writing the assignment...")
    # Imposing on Image
    cnt = 0
    nl = 0
    np = 1
    pdl = []
    img = Image.open("Data/assets/img/ruled1.png")
    for i in text.split('\n'):
        if cnt % 2:
            nl, pdl, np, img = draw(i, True, hwrite, nl, np, uname, img)
        else:
            nl, pdl, np, img = draw(i, False, hwrite, nl, np, uname, img)
        cnt += 1

    try:
        if pdl[0] == pdl[1]:
            pdl.pop(1)
    except:
        pass
    pdf = FPDF()
    # imagelist is the list with all image filenames
    shl = ["l1", "r1"]
    for image in pdl:
        shd = Image.open("Data/assets/img/" + random.choice(shl) + ".png")
        img = Image.open(image).convert("RGBA")
        img.alpha_composite(shd)
        img.save(image)
        if cl == "BW":
            bw = Image.open(image).convert("LA")
            bw.save(image)
        pdf.add_page()
        pdf.set_auto_page_break(0)
        pdf.image(image, w=200)
    pdf.output('Output/' + uname + '.pdf', "F")
    print(pdl)
    print("Successfully Created PDF")
