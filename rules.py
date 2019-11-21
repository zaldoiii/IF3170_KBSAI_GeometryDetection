import clips

env = clips.Environment()

#define facts
fact_sisi_string = """
(deftemplate sisi
    (slot jumlah (type INTEGER)))
"""
env.build(fact_sisi_string)
new_fact = env.find_template('sisi').new_fact()
new_fact['jumlah'] = 4
new_fact.assertit()

fact_polygon_name = """
(deftemplate polygon
    (slot nama (type SYMBOL)))
"""
env.build(fact_polygon_name)

#define rules
rule_sisi_string = """
(defrule define-polygon
    (sisi (jumlah 3))
    =>
    (assert (polygon (nama segitiga))))
"""
env.build(rule_sisi_string)
rule_sisi_string = """
(defrule define-polygon
    (sisi (jumlah 4))
    =>
    (assert (polygon (nama segiempat))))
"""
env.build(rule_sisi_string)
rule_sisi_string = """
(defrule define-polygon
    (sisi (jumlah 5))
    =>
    (assert (polygon (nama segilima))))
"""
env.build(rule_sisi_string)
rule_sisi_string = """
(defrule define-polygon
    (sisi (jumlah 6))
    =>
    (assert (polygon (nama segienam))))
"""
env.build(rule_sisi_string)

#activate rules
#get result
env.run()
