from lib.conn import query
from lib.analysis import obtain_papers

print obtain_papers([u'Xilin Chen', u'Ruiping Wang', u'Zhiwu Huang'], distinct=False)