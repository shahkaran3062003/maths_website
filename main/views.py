from django.shortcuts import render


row = 5


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
        is_detail = True
        x_y = [[], []]
        is_f = False
        is_b = False
        is_on_div = False

        method = request.POST['type']
        point = float(request.POST['point'])

        for j in range(1, row+1):
            x_y[0].append(round(float(request.POST['x'+str(j)]), 2))
            x_y[1].append(round(float(request.POST['y'+str(j)]), 2))

        h = x_y[0][1]-x_y[0][0]
        for i in range(row+1):
            if(point == x_y[0][i]):
                if(method == "Divided"):
                    is_on_div = True
                    x = i+1
                    break
                else:
                    if(i+1 <= row/2):
                        is_f = True
                        x = i+1
                        break
                    elif(i+1 >= row/2):
                        is_b = True
                        x = i+1
                        break
            elif(h > 0):
                if(method == "Divided"):
                    if(point > x_y[0][i] and point < x_y[0][i+1]):
                        x = i+1
                        break
                else:
                    if(point > x_y[0][i] and point < x_y[0][i+1] and i+1 <= row/2):
                        is_f = True
                        x = i+1
                        break
                    elif(point > x_y[0][i] and point < x_y[0][i+1] and i+1 >= row/2):
                        is_b = True
                        x = i+2
                        break
            elif(h < 0):
                if(point < x_y[0][i] and point > x_y[0][i+1] and i+1 <= row/2):
                    is_f = True
                    x = i+1
                    break
                elif(point < x_y[0][i] and point > x_y[0][i+1] and i+1 >= row/2):
                    is_b = True
                    x = i+2
                    break

        if(method != "Divided"):

            u = round((point-x_y[0][x-1])/h, 2)
            # print(h, u, x_y[0], x)

            table = [[0.0 for j in range(row)] for i in range(row)]
            table[0] = x_y[1][:]

            def u_cal(u, n, is_forward):
                temp = u
                if(is_forward):
                    for i in range(1, n):
                        temp = temp*(u-i)

                elif(not is_forward):
                    for i in range(1, n):
                        temp = temp*(u+i)
                return temp

            def diffrence_u_cal(u, n, is_forward):

                u_list = [
                    u-i for i in range(n)] if is_forward else [u+i for i in range(n)]
                # print(u_list)
                ans = 0
                for i in range(n):
                    temp = 1
                    for j in range(n):
                        if(i == j):
                            continue
                        else:
                            temp = temp*u_list[j]
                    ans = ans+temp
                return ans

            def fec(n):
                temp = 1
                for i in range(2, n+1):
                    temp = temp*i
                return temp

            if(is_f):
                for i in range(1, row):
                    for j in range(1, row-i+1):
                        table[i][j-1] = round((table[i-1]
                                               [j]-table[i-1][j-1]), 2)

                    for j in range(row-i+1, row+1):
                        table[i][j-1] = '-'
                table_ = []
                coloum = ['X', 'Y', 'ΔY', 'Δ²Y', 'Δ³Y',
                          'Δ⁴Y', 'Δ⁵Y', 'Δ⁶Y', 'Δ⁷Y', 'Δ⁸Y', 'Δ⁹Y']

                for j in range(len(table[0])):
                    temp = [x_y[0][j]]
                    for i in range(len(table)):
                        temp.append(table[i][j])
                    table_.append(temp)

                if(method == 'simple'):
                    # print(table_, table)
                    ans = table_[x-1][1]
                    # print(table_[x-1])
                    for i in range(1, row):
                        if(table_[x-1][i+1] == '-'):
                            continue
                        temp_u = u_cal(u, i, True)
                        f = fec(i)
                        ans = ans+((table_[x-1][i+1]*temp_u/f))
                        text = f"Here, X = {point} lies between {x} & {x+1} point therefor, we consider newton's Forward Method at {x} point"
                        u_text = f"U = {u}"
                        ans_text = f"ANS = {ans}"

                    return render(request, 'index.html', {"is_rows": is_rows, "is_detail": is_detail, "row": range(1, row+1), "table": table_,
                                                          "column": coloum[:row+1], "text": text, "u_text": u_text, "ans_text": ans_text})
                elif(method == "difference"):
                    if(point in x_y[0]):
                        ans = 0
                        for i in range(1, row):
                            temp = table_[x-1][i+1]/i
                            if(i % 2 == 0):
                                ans = ans-temp
                            else:
                                ans = ans+temp
                        ans = round(ans/h, 3)
                        text = f"Here, X = {point} lies on {x} point therefor, we consider newton's Forward Method at {x} point"
                        u_text = ""
                        ans_text = f"ANS = {ans}"

                        return render(request, 'index.html', {"is_rows": is_rows, "is_detail": is_detail, "row": range(1, row+1), "table": table_,
                                                              "column": coloum[:row+1], "text": text, "u_text": u_text, "ans_text": ans_text})
                    else:
                        ans = table_[x-1][2]

                        for i in range(3, row+1):
                            if(table_[x-1][i] == '-'):
                                continue
                            else:
                                find_u = diffrence_u_cal(u, i-1, True)
                                f = fec(i-1)
                                ans = ans+(table_[x-1][i]*find_u)/f
                                print(
                                    f"{i} = {find_u} , {ans} , {table_[x-1][i]}")
                        ans = round(ans/h, 3)
                        text = f"Here, X = {point} lies between {x} & {x+1} point therefor, we consider newton's Forward Method at {x} point"
                        u_text = f"U = {u}"
                        ans_text = f"ANS = {ans}"

                        return render(request, 'index.html', {"is_rows": is_rows, "is_detail": is_detail, "row": range(1, row+1), "table": table_,
                                                              "column": coloum[:row+1], "text": text, "u_text": u_text, "ans_text": ans_text})

            elif(is_b):
                if(method != "Divided"):
                    for i in range(1, row):
                        for j in range(row-1, i-1, -1):
                            table[i][j] = round(
                                (table[i-1][j]-table[i-1][j-1]), 2)
                        for j in range(i-1+1, 0, -1):
                            table[i][j-1] = '-'

                    table_ = []

                    for j in range(len(table[0])):
                        temp = [x_y[0][j]]
                        for i in range(len(table)):
                            temp.append(table[i][j])
                        table_.append(temp)

                    coloum = ['X', 'Y', '∇Y', '∇²Y', '∇³Y',
                              '∇⁴Y', '∇⁵Y', '∇⁶Y', '∇⁷Y', '∇⁸Y', '∇⁹Y']
                    if(method == 'simple'):
                        # print(table_, table)
                        ans = table_[x-1][1]
                        # print(table_[x-1])
                        for i in range(1, row):
                            if(table_[x-1][i+1] == '-'):
                                continue
                            temp_u = u_cal(u, i, False)
                            f = fec(i)
                            ans = ans+((table_[x-1][i+1]*temp_u/f))
                        ans = round(ans, 3)
                        text = f"Here, X = {point} lies between {x-1} & {x} point therefor, we consider newton's Backward Method at {x} point"
                        u_text = f"U = {u}"
                        ans_text = f"ANS = {ans}"

                        return render(request, 'index.html', {"is_rows": is_rows, "is_detail": is_detail, "row": range(1, row+1), "table": table_,
                                                              "column": coloum[:row+1], "text": text, "u_text": u_text, "ans_text": ans_text})
                    elif(method == 'difference'):
                        if(point in x_y[0]):
                            ans = 0
                            for i in range(1, row):
                                temp = table_[x-1][i+1]/i, 2
                                ans = ans+temp
                            ans = ans/h
                            ans = round(ans, 3)
                            text = f"Here, X = {point} lies on {x} point therefor, we consider newton's Backward Method at {x} point"
                            u_text = ""
                            ans_text = f"ANS = {ans}"

                            return render(request, 'index.html', {"is_rows": is_rows, "is_detail": is_detail, "row": range(1, row+1), "table": table_,
                                                                  "column": coloum[:row+1], "text": text, "u_text": u_text, "ans_text": ans_text})
                        else:
                            ans = table_[x-1][2]

                            for i in range(3, row+1):
                                if(table_[x-1][i] == '-'):
                                    continue
                                else:
                                    find_u = round(
                                        diffrence_u_cal(u, i-1, False), 3)
                                    f = fec(i-1)
                                    ans = ans+(table_[x-1][i]*find_u)/f
                                    print(
                                        f"{i} = {find_u} , {ans} , {table_[x-1][i]},{f}")

                            ans = round(ans/h, 3)
                            text = f"Here, X = {point} lies between {x-1} & {x} point therefor, we consider newton's Backward Method at {x} point"
                            u_text = f"U = {u}"
                            ans_text = f"ANS = {ans}"
                            return render(request, 'index.html', {"is_rows": is_rows, "is_detail": is_detail, "row": range(1, row+1), "table": table_,
                                                                  "column": coloum[:row+1], "text": text, "u_text": u_text, "ans_text": ans_text})
        else:

            def find_x(n):
                temp = 1
                for i in range(n):
                    temp = temp*(point-x_y[0][x+i-1])
                return temp

            table = [[0.0 for j in range(row)] for i in range(row)]
            table[0] = x_y[1][:]
            for i in range(1, row):
                for j in range(1, row-i+1):
                    table[i][j-1] = round((table[i-1]
                                           [j]-table[i-1][j-1])/((x_y[0][j+i-1]-x_y[0][j-1])), 2)

                for j in range(row-i+1, row+1):
                    table[i][j-1] = '-'
            table_ = []
            for j in range(len(table[0])):
                temp = [x_y[0][j]]
                for i in range(len(table)):
                    temp.append(table[i][j])
                table_.append(temp)

            coloum = ['X', 'Y', 'ΔdY', 'Δ²dY', 'Δ³dY',
                      'Δ⁴dY', 'Δ⁵dY', 'Δ⁶dY', 'Δ⁷dY', 'Δ⁸dY', 'Δ⁹dY']
            ans = table_[x-1][1]

            if(not is_on_div):
                for i in range(1, row):
                    if(table_[x-1][i+1] == '-'):
                        continue
                    else:
                        ans += round((table_[x-1][i+1]*find_x(i)), 3)

            text = f"Here, X = {point} lies on {x}  point therefor, we consider newton's Divided Method at {x} point" if (
                is_on_div) else f"Here, X = {point} lies between {x} & {x+1} point therefor, we consider newton's Divided Method at {x} point"
            u_text = ""
            ans_text = f"ANS = {ans}"

            return render(request, 'index.html', {"is_rows": is_rows, "is_detail": is_detail, "row": range(1, row+1), "table": table_, "column": coloum[:row+1],
                                                  "text": text, "u_text": u_text, "ans_text": ans_text})

    else:
        is_rows = False
        is_detail = False
        return render(request, 'index.html')
