from django.shortcuts import render


# Create your views here.

row = None


def main(request):
    is_rows = False
    is_detail = False
    global row
    if 'rows_check' in request.POST:

        row = request.POST['row']
        row = int(row)
        is_rows = True
        return render(request, 'index.html', {"is_rows": is_rows, "is_detail": is_detail, "row": range(1, row+1)})

    elif 'all_details' in request.POST:
        x_y = [[], []]
        is_f = False
        is_b = False

        method = request.POST['type']
        point = float(request.POST['point'])
        for j in range(1, row+1):
            x_y[0].append(round(float(request.POST['x'+str(j)]), 2))
            x_y[1].append(round(float(request.POST['y'+str(j)]), 2))
        is_detail = True
        for i in range(row-1, -1, -1):
            if(point > x_y[0][i] and i+1 <= row/2):
                is_f = True
                x = x_y[0][i]
                break
            elif(point > x_y[0][i] and i+1 >= row/2):
                is_b = True
                x = x_y[0][i+1]
                break
        h = x_y[0][1]-x_y[0][0]
        u = (point-x)/h

        table = [[0 for j in range(row)] for i in range(row)]
        table[0] = x_y[1][:]
        if(is_f):
            for i in range(1, row):
                for j in range(1, row-i+1):
                    table[i][j-1] = table[i-1][j]-table[i-1][j-1]

                for j in range(row-i+1, row+1):
                    table[i][j-1] = '-'
            table_ = []
            coloum = ['S .No', 'X', 'Y', 'Δ²Y', 'Δ³Y',
                      'Δ⁴Y', 'Δ⁵Y', 'Δ⁶Y', 'Δ⁷Y', 'Δ⁸Y', 'Δ⁹Y']

            for j in range(len(table[0])):
                temp = []
                for i in range(len(table)):
                    temp.append(table[i][j])
                table_.append(temp)

        elif(is_b):
            for i in range(1, row):
                for j in range(row-1, i-1, -1):
                    table[i][j] = table[i-1][j]-table[i-1][j-1]
                for j in range(i-1+1, 0, -1):
                    table[i][j-1] = '-'

            table_ = []

            for j in range(len(table[0])):
                temp = []
                for i in range(len(table)):
                    temp.append(table[i][j])
                table_.append(temp)

            coloum = ['S .No', 'X', 'Y', '∇²Y', '∇³Y',
                      '∇⁴Y', '∇⁵Y', '∇⁶Y', '∇⁷Y', '∇⁸Y', '∇⁹Y']

        return render(request, 'index.html', {"is_rows": is_rows, "is_detail": is_detail, "row": range(1, row+1), "table": table_})
    else:
        is_rows = False
        is_detail = False
        return render(request, 'index.html')
