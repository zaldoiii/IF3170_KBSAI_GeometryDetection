import clips

def print_hello():
    print('hello')

def detect_shape(angles, nodes, sides):
    env = clips.Environment()

    #define facts
    fact_sisi_string = """
    (deftemplate sisi
        (slot jumlah (type INTEGER)))
    """
    env.build(fact_sisi_string)
    new_fact = env.find_template('sisi').new_fact()
    new_fact['jumlah'] = len(angles)
    new_fact.assertit()


    fact_polygon_name = """
    (deftemplate polygon
        (slot nama (type SYMBOL))
        (slot tx1 (type INTEGER))
        (slot tx2 (type INTEGER))
        (slot tx3 (type INTEGER))
        (slot tx4 (type INTEGER))
        (slot sisi1 (type FLOAT))
        (slot sisi2 (type FLOAT))
        (slot sisi3 (type FLOAT))
        (slot sisi4 (type FLOAT))
        (slot sisi5 (type FLOAT))
        (slot sisi6 (type FLOAT))
        (slot sudut1 (type FLOAT))
        (slot sudut2 (type FLOAT))
        (slot sudut3 (type FLOAT))
        (slot sudut4 (type FLOAT))
        (slot sudut5 (type FLOAT))
        (slot sudut6 (type FLOAT)))
    """
    env.build(fact_polygon_name)

    #define helping functions
    calculate_error_function = """
    (deffunction acceptable-error
        (?real ?desired ?error)
        (<= (abs (- ?real ?desired)) ?error))
    """
    env.build(calculate_error_function)
    calculate_error_function = """
    (deffunction inequal
        (?arg1 ?arg2 ?error)
        (>= (abs (- ?arg1 ?arg2)) ?error))
    """
    env.build(calculate_error_function)

    #define rules
    #SEGITIGA
    if(len(angles) == 3):
        rule_sisi_string = """
        (defrule define-polygon-segitiga
            (sisi (jumlah 3))
            =>
            (assert (polygon (nama segitiga)))
            (assert (polygon (sudut1 """+str(angles[0])+""")))
            (assert (polygon (sudut2 """+str(angles[1])+""")))
            (assert (polygon (sudut3 """+str(angles[2])+"""))))
        """
        env.build(rule_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-segitiga-sikusiku
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (test (acceptable-error (+ ?s1 ?s2 ?s3) 180.0 3))
            (test (or (acceptable-error ?s1 90.0 1) (acceptable-error ?s2 90.0 1) (acceptable-error ?s3 90.0 1)))
            =>
            (printout t "Polygon: Segitiga Siku-Siku" crlf)
            (assert (polygon (nama segitigasiku-siku))))
        """
        env.build(rule_panjang_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-segitiga-samasisi
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (test (acceptable-error (+ ?s1 ?s2 ?s3) 180.0 3))
            (test (acceptable-error ?s1 60.0 1.0) )
            (test (acceptable-error ?s2 60.0 1.0) )
            (test (acceptable-error ?s3 60.0 1.0) )
            =>
            (printout t "Polygon: Segitiga Sama Sisi" crlf)
            (assert (polygon (nama segitigasamasisi))))
        """
        env.build(rule_panjang_sisi_string)
        

        rule_panjang_sisi_string = """
        (defrule define-segitiga-samakaki
            (not (polygon (nama segitigasamasisi)))
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (test (acceptable-error (+ ?s1 ?s2 ?s3) 180.0 3))
            (test (or (acceptable-error ?s1 ?s2 1.0) (acceptable-error ?s1 ?s3 1.0) (acceptable-error ?s3 ?s2 1.0)))
            =>
            (printout t "Polygon: Segitiga Sama Kaki" crlf)
            (assert (polygon (nama segitigasamakaki))))
        """
        env.build(rule_panjang_sisi_string)

        rule_panjang_sisi_string = """
        (defrule define-segitiga-tumpul
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (test (acceptable-error (+ ?s1 ?s2 ?s3) 180.0 3))
            (test (or (> ?s1 90.0) (> ?s2 90.0) (> ?s3 90.0)))
            =>
            (printout t "Polygon: Segitiga Tumpul" crlf)
            (assert (polygon (nama segitigatumpul))))
        """
        env.build(rule_panjang_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-segitiga-lancip
            (not (polygon (nama segitigasamasisi)))
            (not (polygon (nama segitigasamakaki)))
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (test (acceptable-error (+ ?s1 ?s2 ?s3) 180.0 3))
            (test (and (< ?s1 90.0) (< ?s2 90.0) (< ?s3 90.0)))
            =>
            (printout t "Polygon: Segitiga Lancip" crlf)
            (assert (polygon (nama segitigalancip))))
        """
        env.build(rule_panjang_sisi_string)
    


    #SEGIEMPAT
    if(len(angles) == 4):
        rule_sisi_string = """
        (defrule define-polygon-segiempat
            (sisi (jumlah 4))
            =>
            (printout t "Polygon: Segi Empat" crlf)
            (assert (polygon (nama segiempat)))
            (assert (polygon (sudut1 """+str(angles[0])+""")))    
            (assert (polygon (sudut2 """+str(angles[1])+""")))
            (assert (polygon (sudut3 """+str(angles[2])+""")))
            (assert (polygon (sudut4 """+str(angles[3])+""")))
            (assert (polygon (sisi1 """+str(sides[0])+""")))
            (assert (polygon (sisi2 """+str(sides[1])+""")))
            (assert (polygon (sisi3 """+str(sides[2])+""")))
            (assert (polygon (sisi4 """+str(sides[3])+""")))
            (assert (polygon (tx1 """+str(nodes[0][0])+""")))
            (assert (polygon (tx2 """+str(nodes[1][0])+""")))
            (assert (polygon (tx3 """+str(nodes[2][0])+""")))
            (assert (polygon (tx4 """+str(nodes[3][0])+""")))
            )
        """
        env.build(rule_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-segiempat-beraturan
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (polygon (sudut4 ?s4))
            (test (acceptable-error (+ ?s1 ?s2 ?s3 ?s4) 360.0 3))
            (test (acceptable-error ?s1 ?s2 2))
            (test (acceptable-error ?s2 ?s3 2))
            (test (acceptable-error ?s3 ?s4 2))
            (test (acceptable-error ?s1 ?s4 2)) 
            =>
            (printout t "Polygon: Segi Empat Beraturan" crlf)
            (assert (polygon (nama segiempatberaturan))))
        """
        env.build(rule_panjang_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-segiempat-layang-layang
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (polygon (sudut4 ?s4))
            (test (acceptable-error (+ ?s1 ?s2 ?s3 ?s4) 360.0 5))
            (or
                (test(and (acceptable-error ?s1 ?s3 3) (inequal ?s2 ?s4 3)))
                (test(and (acceptable-error ?s2 ?s4 3) (inequal ?s1 ?s3 3)))
            )
            =>
            (printout t "Polygon: Segi Empat Layang-Layang" crlf)
            (assert (polygon (nama segiempatlayanglayang))))
        """
        env.build(rule_panjang_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-trapesium-samakaki
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (polygon (sudut4 ?s4))
            (test (acceptable-error (+ ?s1 ?s2 ?s3 ?s4) 360.0 5))
            (or
                (test(and (acceptable-error ?s2 ?s3 1) (inequal ?s1 ?s2 1)))
                (test(and (acceptable-error ?s2 ?s1 1) (inequal ?s2 ?s3 1)))
            )
            =>
            (printout t "Polygon: Trapesium Sama Kaki" crlf)
            (assert (polygon (nama trapesiumsamakaki))))
        """
        env.build(rule_panjang_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-trapesium-samakaki
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (polygon (sudut4 ?s4))
            (test (acceptable-error (+ ?s1 ?s2 ?s3 ?s4) 360.0 5))
            (or
                (test(and (acceptable-error ?s2 ?s3 1) (inequal ?s1 ?s2 1)))
                (test(and (acceptable-error ?s2 ?s1 1) (inequal ?s2 ?s3 1)))
            )
            =>
            (printout t "Polygon: Trapesium Sama Kaki" crlf)
            (assert (polygon (nama trapesiumsamakaki))))
        """
        env.build(rule_panjang_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-trapesium-rata
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (polygon (sudut4 ?s4))
            (test (acceptable-error (+ ?s1 ?s2 ?s3 ?s4) 360.0 5))
            (and
                (test(or (acceptable-error ?s1 90.0 3) (acceptable-error ?s3 90.0 3)))
                (test(or (acceptable-error ?s2 90.0 3) (acceptable-error ?s4 90.0 3)))
            )
            =>
            (printout t "Polygon: Trapesium Rata" crlf)
            (assert (polygon (nama trapesiumrata))))
        """
        env.build(rule_panjang_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-trapesium-rata-kiri
            (polygon (tx1 ?s1))
            (polygon (tx2 ?s2))
            (polygon (tx3 ?s3))
            (polygon (tx4 ?s4))
            (polygon (nama trapesiumrata))
            (or
                (test(and (acceptable-error ?s1 ?s2 4) (< ?s2 ?s3)))
                (test(and (acceptable-error ?s2 ?s3 4) (< ?s3 ?s4)))
                (test(and (acceptable-error ?s3 ?s4 4) (< ?s4 ?s1)))
                (test(and (acceptable-error ?s4 ?s1 4) (< ?s1 ?s2)))
            )
            
            =>
            (printout t "Polygon: Trapesium Rata Kiri" crlf)
            (assert (polygon (nama trapesiumratakiri))))
        """
        env.build(rule_panjang_sisi_string)

        rule_panjang_sisi_string = """
        (defrule define-trapesium-rata-kanan
            (polygon (tx1 ?s1))
            (polygon (tx2 ?s2))
            (polygon (tx3 ?s3))
            (polygon (tx4 ?s4))
            (polygon (nama trapesiumrata))
            (not (polygon (nama trapesiumratakiri)))
            (or
                (test(and (acceptable-error ?s1 ?s2 5) (> ?s2 ?s3)))
                (test(and (acceptable-error ?s2 ?s3 5) (> ?s3 ?s4)))
                (test(and (acceptable-error ?s3 ?s4 5) (> ?s4 ?s1)))
                (test(and (acceptable-error ?s4 ?s1 5) (> ?s1 ?s2)))
            )
            =>
            (assert (polygon (nama trapesiumratakanan))))
            (printout t "Polygon: Trapesium Rata Kanan" crlf)
        """
        env.build(rule_panjang_sisi_string)
    if(len(angles) == 5):
        #SEGILIMA
        rule_sisi_string = """
        (defrule define-polygon-segilima
            (sisi (jumlah 5))
            =>
            (printout t "Polygon: Segi Lima" crlf)
            (assert (polygon (nama segilima))))
        """
        env.build(rule_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-segienam-samasisi
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (polygon (sudut4 ?s4))
            (polygon (sudut5 ?s5))
            (test (acceptable-error ?s1 72.0 1.0) )
            (test (acceptable-error ?s2 72.0 1.0) )
            (test (acceptable-error ?s3 72.0 1.0) )
            (test (acceptable-error ?s4 72.0 1.0) )
            (test (acceptable-error ?s5 72.0 1.0) )
            =>
            (printout t "Polygon: Segi Lima Sama Sisi" crlf)
            (assert (polygon (nama segilimasamasisi))))
        """
        env.build(rule_panjang_sisi_string)
    

    if(len(angles) == 6):
        #SEGIENAM
        rule_sisi_string = """
        (defrule define-polygon-segienam
            (sisi (jumlah 6))
            =>
            (printout t "Polygon: Segi Enam" crlf)
            (assert (polygon (nama segienam))))
        """
        env.build(rule_sisi_string)
        rule_panjang_sisi_string = """
        (defrule define-segienam-samasisi
            (polygon (sudut1 ?s1))
            (polygon (sudut2 ?s2))
            (polygon (sudut3 ?s3))
            (polygon (sudut4 ?s4))
            (polygon (sudut5 ?s5))
            (polygon (sudut6 ?s6))
            (test (acceptable-error ?s1 60.0 1.0) )
            (test (acceptable-error ?s2 60.0 1.0) )
            (test (acceptable-error ?s3 60.0 1.0) )
            (test (acceptable-error ?s4 60.0 1.0) )
            (test (acceptable-error ?s5 60.0 1.0) )
            (test (acceptable-error ?s6 60.0 1.0) )
            =>
            (printout t "Polygon: Segi Enam Sama Sisi" crlf)
            (assert (polygon (nama segienamsamasisi))))
        """
        env.build(rule_panjang_sisi_string)
    

    #check existing rules 
    # for rule in env.rules():
    #     print(rule)

    #activate rules
    #get result
    # for activation in  env.activations():
    #     print(activation)
    env.run()
    # for fact in  env.facts():
    #     print(fact)
    
