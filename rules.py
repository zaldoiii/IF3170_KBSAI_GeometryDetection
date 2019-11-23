import clips

env = clips.Environment()

angles = [60.1409838350769, 59.91349544599977, 59.945520718923326]

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

calculate_error_function = """
(deffunction acceptable-error
    (?real ?desired ?error)
    (<= (abs (- ?real ?desired)) ?error))
"""
env.build(calculate_error_function)

#define rules
#SEGITIGA
rule_sisi_string = """
(defrule define-polygon-segitiga
    (sisi (jumlah 3))
    =>
    (printout t "Polygon: Segitiga" crlf)
    (assert (polygon (nama segitiga)))
    (assert (polygon (sisi1 """+str(angles[0])+""")))
    (assert (polygon (sisi2 """+str(angles[1])+""")))
    (assert (polygon (sisi3 """+str(angles[2])+"""))))
"""
env.build(rule_sisi_string)
rule_panjang_sisi_string = """
(defrule define-segitiga-sikusiku
    (polygon (sisi1 ?s1))
    (polygon (sisi2 ?s2))
    (polygon (sisi3 ?s3))
    (test (acceptable-error (+ ?s1 ?s2 ?s3) 180.0 0.5))
    (test (or (acceptable-error ?s1 90.0 0.1) (acceptable-error ?s2 90.0 0.5) (acceptable-error ?s3 90.0 0.5)))
    =>
    (printout t "Polygon: Segitiga Siku-Siku" crlf)
    (assert (polygon (nama segitigasiku-siku))))
"""
env.build(rule_panjang_sisi_string)
#SEGIEMPAT
rule_sisi_string = """
(defrule define-polygon-segiempat
    (sisi (jumlah 4))
    =>
    (assert (polygon (nama segiempat))))
"""
env.build(rule_sisi_string)
rule_sisi_string = """
(defrule define-polygon-segilima
    (sisi (jumlah 5))
    =>
    (assert (polygon (nama segilima))))
"""
env.build(rule_sisi_string)
rule_sisi_string = """
(defrule define-polygon-segienam
    (sisi (jumlah 6))
    =>
    (assert (polygon (nama segienam))))
"""
env.build(rule_sisi_string)

#check existing rules 
# for rule in env.rules():
#     print(rule)

#activate rules
#get result
for activation in  env.activations():
    print(activation)
env.run()
