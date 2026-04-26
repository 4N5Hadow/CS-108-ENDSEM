import sys, importlib.util, os as _os
R="\033[1;31m";G="\033[1;32m";Y="\033[1;33m";D="\033[2;37m";B="\033[1m";X="\033[0m"
def _load():
    try:
        _p=_os.path.join(_os.getcwd(),"vision_shell.py")
        spec=importlib.util.spec_from_file_location("s",_p)
        mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
    except SyntaxError as e:
        print("\n"+R+"Syntax error line "+str(e.lineno)+": "+str(e.msg)+X+"\n"); sys.exit(1)
    except Exception as e:
        print("\n"+R+"Cannot load vision_shell.py: "+str(e)+X+"\n"); sys.exit(1)
def _r(fn,m):
    try: fn(); return m
    except: return 0
def main():
    mod=_load(); FS=mod.FileSystem; VC=mod.VersionControl; NS=mod.NexusShell
    def _1a():
        fs=FS(); fs.cd('/'); fs.mkdir('/ops'); fs.cd('ops')
        assert fs.pwd()=='/ops'
    def _1b():
        fs=FS(); fs.cd('/'); assert fs.read('home')==''
    def _1c():
        fs=FS(); fs.touch('zebra.txt'); fs.touch('alpha.txt')
        l=fs.ls(); assert l==sorted(l)
    def _1d():
        fs=FS(); log='resistance is live\nNOVA wins\nresistance fights back'
        assert fs.grep('resistance',log)=='resistance is live\nresistance fights back'
    def _1e():
        fs=FS()
        fs.mkdir('/tmp')
        assert 'tmp' in fs._get_node('/')['children']
        assert 'tmp' not in fs._get_node('/home/sushant')['children']
        fs.mkdir('/home/sushant/ops')
        fs.mkdir('/home/sushant/ops/deep')
        fs.cd('/home/sushant/ops/deep')
        fs.touch('t.txt'); fs.write('t.txt','signal')
        assert fs.read('t.txt')=='signal'
        fs.cd('..'); assert 'deep' in fs.ls()
    p1=sum(_r(f,1) for f in [_1a,_1b,_1c,_1d,_1e])
    def _2a():
        fs=FS(); vc=VC(fs); vc.add('/home/sushant/nova_log.txt')
        assert '/home/sushant/nova_log.txt' in vc.status()['staged']
    def _2b():
        fs=FS(); vc=VC(fs); assert vc.commit('a')==1; assert vc.commit('b')==2
        assert vc.status()['staged']==[]
    def _2c():
        fs=FS(); vc=VC(fs); fs.write('nova_log.txt','v1')
        vc.add('/home/sushant/nova_log.txt'); vc.commit('v1')
        vc.branch('dev'); vc.checkout('dev'); fs.write('nova_log.txt','v2')
        vc.add('/home/sushant/nova_log.txt'); vc.commit('v2')
        vc.checkout('main'); assert fs.read('nova_log.txt')=='v1'
    def _2d():
        fs=FS(); vc=VC(fs); fs.write('nova_log.txt','original')
        vc.add('/home/sushant/nova_log.txt'); vc.commit('snap')
        fs.write('nova_log.txt','CORRUPTED'); vc.checkout('main')
        assert fs.read('nova_log.txt')=='original'
    p2=_r(_2a,0.5)+_r(_2b,1.5)+_r(_2c,1.5)+_r(_2d,1.5)
    def _3a():
        sh=NS(); sh.run('mkdir /home/sushant/ops'); sh.run('cd /home/sushant/ops')
        assert sh.run('pwd')=='/home/sushant/ops'
    def _3b():
        sh=NS(); sh.run('echo nova patch v2 > patch.txt')
        assert sh.run('cat patch.txt')=='nova patch v2'
    def _3c():
        sh=NS(); sh.fs.write('nova_log.txt','NOVA line 1\nNOVA off\nNOVA line 2')
        assert sh.run('cat nova_log.txt | grep NOVA')=='NOVA line 1\nNOVA off\nNOVA line 2'
        sh2=NS(); sh2.fs.write('nova_log.txt','NOVA line 1\nother\nNOVA line 2')
        assert sh2.run('cat nova_log.txt | grep other')=='other'
    def _3d():
        sh=NS(); sh.run('git add /home/sushant/nova_log.txt')
        assert sh.run('git commit "a"')=='Committed as ID 1'
        assert sh.run('git commit "b"')=='Committed as ID 2'
    def _3e():
        sh=NS(); sh.run('cd /'); sh.run('mkdir /ops'); sh.run('cd /ops'); sh.run('cd ..')
        assert sh.run('pwd')=='/'; assert 'ops' in (sh.run('ls') or '')
    p3=_r(_3a,1.0)+_r(_3b,1.0)+_r(_3c,2.0)+_r(_3d,0.5)+_r(_3e,0.5)
    total=p1+p2+p3; p1_pub=min(p1,4)
    col=G if (p1_pub+p2+p3)/14*100>=80 else (Y if (p1_pub+p2+p3)/14*100>=50 else R)
    def bar(s,mx,w=20):
        f=round(s/mx*w) if mx>0 else 0; return G+"\u2588"*f+D+"\u2591"*(w-f)+X
    TL="\u2554"; TR="\u2557"; BL="\u255a"; BR="\u255d"; V="\u2551"
    SEP="\u2550"*42; HSEP="\u2500"*52
    t1="  VISION OS  \u2014  Status Check"
    t2="  Ansh is holding. Shanmathi is watching."
    print()
    print("  "+B+TL+SEP+TR+X)
    print("  "+B+V+t1.center(42)+V+X)
    print("  "+D+V+t2.center(42)+V+X)
    print("  "+B+BL+SEP+BR+X)
    print()
    print("  "+"Part 1  [Bug Hunt]".ljust(28)+"  "+bar(p1_pub,4)+"  "+col+"%.2f"%p1_pub+X+" / 4  "+D+"(+1 hidden)"+X)
    print("  "+"Part 2  [VersionControl]".ljust(28)+"  "+bar(p2,5)+"  "+col+"%.2f"%p2+X+" / 5")
    print("  "+"Part 3  [NexusShell]".ljust(28)+"  "+bar(p3,5)+"  "+col+"%.2f"%p3+X+" / 5")
    print("  "+D+HSEP+X)
    print("  "+"Total (visible)".ljust(28)+"  "+bar(p1_pub+p2+p3,14)+"  "+col+B+"%.2f"%(p1_pub+p2+p3)+X+" / 14")
    print()
    print("  "+D+"  Public tests are references only. Write your own edge cases."+X)
    print("  "+D+"  Public tests may change for final scoring."+X)
    print()
if __name__=='__main__': main()
