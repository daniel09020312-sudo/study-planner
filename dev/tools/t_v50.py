# 웹 경로에서 내가 기록을 바꾸면 점수가 바로 반영되는지(점수 캐시)
import os, sys, json, datetime, time
src = open('/home/claude/planner/tools/perf50w.py', encoding='utf-8').read().split("print('ready'")[0]
exec(src)
TD = '2026-11-25'
def sc(): return ev(B, "(()=>{const r=__gbb.view().sc['m1']['%s'];return r?[r.total,r.done,r.mins,r.att]:null})()" % TD)
a = sc(); print('before', a)
B.evaluate("()=>{__gbb.editDay('%s',function(d){d.goals=[{id:'z1',text:'a',sid:'s1',done:true},{id:'z2',text:'b',sid:'s1',done:true},{id:'z3',text:'c',sid:'s1',done:true}];d.mins={s1:300};d.in=new Date().toISOString();});}" % TD)
B.wait_for_timeout(600)
b = sc(); print('after local edit', b)
B.wait_for_timeout(2500)
c = sc(); print('after sync echo', c)
print('changed', a != b, 'stable', b == c)
print('errors', errors)
# 다시 열기(저장해 둔 기록으로 열림) 뒤에도 반영되는지
B.reload(); B.wait_for_timeout(3500); closepin(B)
d0 = sc(); print('after reload', d0)
B.evaluate("()=>{__gbb.editDay('%s',function(d){d.mins={s1:420};});}" % TD)
B.wait_for_timeout(800)
d1 = sc(); print('after edit #2', d1, 'changed', d0 != d1)
server_set('days/m1_' + TD, {'goals': [], 'mins': {'s1': 10}, 'in': TD + 'T00:10:00.000Z'})
B.wait_for_timeout(3000)
d2 = sc(); print('after remote', d2, 'changed', d1 != d2)
print('errors', errors)
