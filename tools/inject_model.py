# Embeds a model exported by tools/alien_blender.py into index.html as `var MDL_<NAME>=...;`
#   python3 tools/inject_model.py ALIEN alien.json
import sys, re
name, path = sys.argv[1], sys.argv[2]
s = open('index.html').read(); line = 'var MDL_%s=%s;\n' % (name, open(path).read().strip())
pat = re.compile(r'^var MDL_%s=.*\n' % name, re.M)
if pat.search(s): s = pat.sub(lambda m: line, s, count=1)
else:
    i = s.index('var I18N='); s = s[:i] + line + s[i:]
open('index.html', 'w').write(s); print('embedded', name, len(line) // 1024, 'KB')
