class MatheService:
    def __init__(self):
        pass

    def p_sum(self, lst):
        return sum(lst)

    def p_join(self, lst, st):
        return st.join([str(l) for l in lst])

