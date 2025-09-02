from flask import Flask, render_template, request

app = Flask(__name__)

def formatear_conjunto(conjunto):
    if not conjunto:
        return "{}"
    return "{" + ",".join(conjunto) + "}"

def crear_conjunto(texto):
    if not texto:
        return []
    return list(dict.fromkeys(texto.split(",")))

@app.route("/", methods=["GET", "POST"])
def home():
    resultado = None      
    mensaje = ""
    estado = "info" 
    operacion = request.form.get("operacion")
    categoria = request.form.get("categoria")

    if request.method == "POST" and operacion:
        A = crear_conjunto(request.form.get("A", ""))
        B = crear_conjunto(request.form.get("B", ""))

        # Pertenencia
        if operacion == "pertenencia":
            elem = request.form.get("elem", "")
            if not elem:
                mensaje, resultado, estado = "Debe ingresar un elemento.", "{}", "danger"
            else:
                pertenece_A, pertenece_B = elem in A, elem in B
                if pertenece_A and pertenece_B:
                    mensaje, resultado = f"El elemento {elem} pertenece a A: {formatear_conjunto(A)} y B: {formatear_conjunto(B)}.", " C: {"+elem+"}"
                elif pertenece_A:
                    mensaje, resultado = f"El elemento {elem} pertenece solo a A: {formatear_conjunto(A)}", "C: {"+elem+"}"
                elif pertenece_B:
                    mensaje, resultado = f"El elemento {elem} pertenece solo a B: {formatear_conjunto(B)}", " C:{"+elem+"}"
                else:
                    mensaje, resultado, estado = f"El elemento {elem} no pertenece a A: {formatear_conjunto(A)} ni a B: {formatear_conjunto(B)}.", "se devuelve un resultado vacio{}", "danger"

        # Unión
        elif operacion == "union":
            if not A and not B:
                mensaje, resultado, estado = "Debe ingresar conjuntos válidos.", "{}", "danger"
            else:
                union = list(dict.fromkeys(A + B))
                resultado = formatear_conjunto(union)
                mensaje = f"El resultado de la unión entre A: {formatear_conjunto(A)} y B: {formatear_conjunto(B)} es: C:"

        # Intersección
        elif operacion == "interseccion":
            inter = [x for x in A if x in B]
            if inter:
                resultado = formatear_conjunto(inter)
                mensaje = f"El resultado de la intersección A: {formatear_conjunto(A)} y B: {formatear_conjunto(B)} es: C:"
            else:
                mensaje, resultado, estado = "No hay intersección, el conjunto es vacío.", "{}", "danger"

        # Complemento
        elif operacion == "complemento":
            conjA = crear_conjunto(request.form.get("conjuntoA", ""))
            if not conjA:
                mensaje, resultado, estado = "Debe ingresar un conjunto válido.", "{}", "danger"
            else:
                comp = [x for x in conjA if x not in B]
                if comp:
                    resultado = formatear_conjunto(comp)
                    mensaje = f"El complemento de B: {formatear_conjunto(B)} respecto a A: {formatear_conjunto(conjA)} es: C:"
                else:
                    mensaje, resultado, estado = "El complemento es vacío.", "{}", "danger"

        # Diferencia
        elif operacion == "diferencia":
            if not A and not B:
                mensaje, resultado, estado = "Debe ingresar conjuntos válidos.", "{}", "danger"
            else:
                dif = [x for x in A if x not in B]
                if dif:
                    resultado = formatear_conjunto(dif)
                    mensaje = f"El resultado de la diferencia A: {formatear_conjunto(A)} - B: {formatear_conjunto(B)} es: C:"
                else:
                    mensaje, resultado, estado = "No hay diferencia, el conjunto es vacío.", "{}", "danger"

        # Diferencia Simétrica
        elif operacion == "diferencia_sim":
            if not A and not B:
                mensaje, resultado, estado = "Debe ingresar conjuntos válidos.", "{}", "danger"
            else:
                dif_sim = [x for x in A if x not in B] + [x for x in B if x not in A]
                if dif_sim:
                    resultado = formatear_conjunto(dif_sim)
                    mensaje = f"El resultado de la diferencia simétrica entre A: {formatear_conjunto(A)} y B: {formatear_conjunto(B)} es: C:"
                else:
                    mensaje, resultado, estado = "No hay diferencia simétrica, el conjunto es vacío.", "{}", "danger"

        # ============================
        #  OPERACIONES de CADENAS
        # ============================
        
        
        #longitud
        if operacion == "longitud":
            cadena = request.form.get("cadena", "")
            if not cadena:
                mensaje, resultado, estado = "Debe ingresar una cadena.", "{}", "danger"
            else:
                resultado = f"{{{cadena}}} = {{{len(cadena)}}}"
                mensaje = f"La longitud de la cadena es {len(cadena)} caracteres."
        
        #concatenación
        elif operacion == "concatenación":
            cadena1 = request.form.get("cadena1", "")
            cadena2 = request.form.get("cadena2", "")
            if not cadena1 or not cadena2:
                mensaje, resultado, estado = "Debe ingresar ambas cadenas.", "{}", "danger"
            else:
                resultado = f"{{{cadena1 + cadena2}}}"
                mensaje = f"La concatenación de {{{cadena1}}} y {{{cadena2}}} es:"

        #potenciacion
        elif operacion == "potenciación":
            cadena = request.form.get("cadena", "")
            potencia = request.form.get("potencia", "0")
            try:
                n = int(potencia)
                if not cadena:
                    mensaje, resultado, estado = "Debe ingresar una cadena.", "{}", "danger"
                elif n < 0:
                    mensaje, resultado, estado = "La potencia debe ser un número entero positivo.", "{}", "danger"
                else:
                    resultado = f"{{{cadena * n}}}"
                    mensaje = f"La cadena {{{cadena}}} elevada a la potencia {n} es:"
            except ValueError:
                mensaje, resultado, estado = "La potencia debe ser un número entero.", "{}", "danger"


        #reflexión
        elif operacion == "reflexión":
            cadena = request.form.get("cadena", "")
            if not cadena:
                mensaje, resultado, estado = "Debe ingresar una cadena.", "{}", "danger"
            else:
                resultado = f"{{{cadena[::-1]}}}"
                mensaje = f"La reflexión (inversa) de la cadena {{{cadena}}} es:"

        # ============================
        #  OPERACIONES de LENGUAJES
        # ============================


        #concatenación
        elif operacion == "concatenación_lenguajes":
            if not A or not B:
                mensaje, resultado, estado = "Debe ingresar dos lenguajes válidos.", "{}", "danger"
            else:
                concat = [x + y for x in A for y in B]
                resultado = formatear_conjunto(concat)
                mensaje = f"El resultado de la concatenación de L1: {formatear_conjunto(A)} y L2: {formatear_conjunto(B)} es:"


        #potenciación
        elif operacion == "potenciación_lenguajes":
            potencia = request.form.get("potencia", "0")
            try:
                n = int(potencia)
                if not A:
                    mensaje, resultado, estado = "Debe ingresar un lenguaje válido.", "{}", "danger"
                elif n < 0:
                    mensaje, resultado, estado = "La potencia debe ser un número entero positivo.", "{}", "danger"
                elif n == 0:
                    resultado = "{ε}"
                    mensaje = f"El lenguaje elevado a la potencia {n} es:"
                else:
                    pot = A.copy()
                    for _ in range(n-1):
                        pot = [x + y for x in pot for y in A]
                    resultado = formatear_conjunto(pot)
                    mensaje = f"El lenguaje {formatear_conjunto(A)} elevado a la potencia {n} es:"
            except ValueError:
                mensaje, resultado, estado = "La potencia debe ser un número entero.", "{}", "danger"

        #reflexión
        elif operacion == "reflexión_lenguajes":
            if not A:
                mensaje, resultado, estado = "Debe ingresar un lenguaje válido.", "{}", "danger"
            else:
                reflejado = [cadena[::-1] for cadena in A]
                resultado = formatear_conjunto(reflejado)
                mensaje = f"La reflexión (inversa) del lenguaje {formatear_conjunto(A)} es:"

        #unión
        elif operacion == "unión_lenguajes":
            if not A and not B:
                mensaje, resultado, estado = "Debe ingresar dos lenguajes válidos.", "{}", "danger"
            else:
                union = list(dict.fromkeys(A + B))
                resultado = formatear_conjunto(union)
                mensaje = f"La unión de L1: {formatear_conjunto(A)} y L2: {formatear_conjunto(B)} es:"

         #intersección
        elif operacion == "intersección_lenguajes":
            inter = [x for x in A if x in B]
            if inter:
                resultado = formatear_conjunto(inter)
                mensaje = f"La intersección de L1: {formatear_conjunto(A)} y L2: {formatear_conjunto(B)} es:"
            else:
                mensaje, resultado, estado = "No hay intersección, el lenguaje es vacío.", "{}", "danger"

        #resta
        elif operacion == "resta":
            if not A and not B:
                mensaje, resultado, estado = "Debe ingresar dos lenguajes válidos.", "{}", "danger"
            else:
                resta = [x for x in A if x not in B]
                if resta:
                    resultado = formatear_conjunto(resta)
                    mensaje = f"La resta L1 - L2 = {formatear_conjunto(A)} - {formatear_conjunto(B)} es:"
                else:
                    mensaje, resultado, estado = "No hay diferencia, el lenguaje es vacío.", "{}", "danger"

        #kleene
        elif operacion == "kleene":
            limite = request.form.get("limite", "0")
            try:
                n = int(limite)
                if not A:
                    mensaje, resultado, estado = "Debe ingresar un lenguaje válido.", "{}", "danger"
                elif n <= 0:
                    mensaje, resultado, estado = "El límite es 0 por lo tanto se devuelve vacío.", "{λ}", "danger"
                else:
                    kleene = [""]
                    actual = A.copy()
                    for i in range(1, n+1):
                        if i == 1:
                            kleene += A
                        else:
                            actual = [x + y for x in actual for y in A]
                            kleene += actual
                    kleene_mostrado = ["λ" if x == "" else x for x in kleene]
                    resultado = "{" + ", ".join(dict.fromkeys(kleene_mostrado)) + ", ...}"
                    mensaje = f"La clausura de Kleene de {formatear_conjunto(A)} hasta {n} concatenaciones es:"
            except ValueError:
                mensaje, resultado, estado = "El límite debe ser un número entero.", "{}", "danger"

        #positiva
        elif operacion == "positiva":
            limite = request.form.get("limite", "0")
            try:
                n = int(limite)
                if not A:
                    mensaje, resultado, estado = "Debe ingresar un lenguaje válido.", "{}", "danger"
                elif n <= 0:
                    mensaje, resultado, estado = "El límite debe ser mayor que cero.", "{}", "danger"
                else:
                    positiva = []
                    actual = A.copy()
                    for i in range(1, n+1):
                        if i == 1:
                            positiva += A
                        else:
                            actual = [x + y for x in actual for y in A]
                            positiva += actual
                    resultado = "{" + ", ".join(dict.fromkeys(positiva)) + ", ...}"
                    mensaje = f"La clausura positiva de {formatear_conjunto(A)} hasta {n} concatenaciones es:"
            except ValueError:
                mensaje, resultado, estado = "El límite debe ser un número entero.", "{}", "danger"

    return render_template("index.html", categoria=categoria, operacion=operacion, resultado=resultado, mensaje=mensaje, estado=estado)


if __name__ == "__main__":
    app.run(debug=True)
