import math, numpy

# An implementation of Dunning's loglikelihood based on this blog post:
# http://tdunning.blogspot.com.au/2008/03/surprise-and-coincidence.html

def c_to_m(f12, f1, f2, N):
    a = f12
    b = f2 - a
    c = f1 - a
    d = N - a - b - c
    assert f12 == a
    assert f2 == a + b
    assert f1 == a + c
    assert N == a + b + c + d
    return numpy.matrix([[a,b],[c,d]], dtype='int64')

def LLR(f12, f1, f2, N):
    return LLR_helper(c_to_m(f12, f1, f2, N))
    
def m_to_a(m):
    # Convert a matrix to a list
    return list(m.flat)

def LLR_helper(k):
    # k is a (numpy) co-occurrence matrix (I've only tried this with the 2x2 case...)
    col_sums = k.sum(axis=0)
    row_sums = k.sum(axis=1)
    return 2 * k.sum() * (H(m_to_a(k)) - H(m_to_a(row_sums)) - H(m_to_a(col_sums)))

def H(k):
    N = float(sum(k))
    return sum([(x / N) * math.log(x / N + int(x == 0)) for x in k])

def llr2(a, b, c, d, signed_root=False):
    # An alternative implementation
    # Compute LLR for a 2x2 matrix of the form
    #
    # a b 
    # c d
    #
    # For cross-corpus comparison cases the columns would typically
    # represent corpora (in the notation that most sources seem to use)
    # So it would be
    # freq_w_in_c1 freq_w_in_c2
    # freq_not_w_in_c1 freq_not_w_in_c2

    def xlnx(x):
        if x == 0:
            return 0
        else:
            return x * math.log(x)
    result = 2 * (xlnx(a) + xlnx(b) + xlnx(c) + xlnx(d) + xlnx(a + b + c+ d) - xlnx(a + b) - xlnx(a + c) - xlnx(b + d) - xlnx(c + d))

    # This is slightly different from the implementation in 
    # apache.commons.math3.stat.inference.GTest.java
    # http://svn.apache.org/viewvc/commons/proper/math/trunk/src/main/java/org/apache/commons/math3/stat/inference/GTest.java?view=markup
    # In that implementation they comapre a/(a+b) < c/(c+d)

    # I think these are equivalent, but what I've implemented is much
    # more intuitive.

    if signed_root:
        sign = 1
        if a / float(a + c) < b / float(b + d):
            sign = -1
        result = sign * math.sqrt(result)

    return result

if __name__ == '__main__':
    
    # Tests for LL based on Dunning's comments here:
    # https://gist.github.com/805773

    eps = 0.001

    assert 0.08043486 - eps < LLR_helper(numpy.matrix([[1,2],[3,4]])) < 0.08043486 + eps 
    assert 2.772589 - eps < LLR_helper(numpy.matrix([[1,0],[0,1]])) < 2.772589 + eps
    assert 27.72589 - eps < LLR_helper(numpy.matrix([[10,0],[0,10]])) < 27.72589 + eps
    assert 34.25049 - eps < LLR_helper(numpy.matrix([[2,0],[1,10000]])) < 34.25049  + eps
    assert 24.24724 - eps < LLR_helper(numpy.matrix([[2,8],[1,10000]])) < 24.24724 + eps

    assert 0.08043486 - eps < llr2(1,2,3,4) < 0.08043486 + eps 
    assert 2.772589 - eps < llr2(1,0,0,1) < 2.772589 + eps
    assert 27.72589 - eps < llr2(10,0,0,10) < 27.72589 + eps
    assert 34.25049 - eps < llr2(2,0,1,10000) < 34.25049  + eps
    assert 24.24724 - eps < llr2(2,8,1,10000) < 24.24724 + eps

    assert math.sqrt(24.24724 - eps) < llr2(2,8,1,10000,signed_root=True) < math.sqrt(24.24724 + eps)
    assert -math.sqrt(24.24724 + eps) < llr2(8,2,10000,1,signed_root=True) < -math.sqrt(24.24724 - eps)


    assert (c_to_m(1, 4, 3, 10) == numpy.matrix([[1,2],[3,4]])).all()
    assert (c_to_m(2, 3, 2, 10003) == numpy.matrix([[2,0],[1,10000]])).all()

    assert LLR_helper(numpy.matrix([[1,2],[3,4]])) == LLR(1,4,3,10)
    assert LLR_helper(numpy.matrix([[2,0],[1,10000]])) == LLR(2, 3, 2, 10003)
