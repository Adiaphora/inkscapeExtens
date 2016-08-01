#!/usr/bin/env python
import simplestyle as ss, inkex

elems=('path','circle','ellipse','rect','polygon','line')
colortags=('fill','stroke')
palette=[]

def walk(node):
  checkStyle(node)
  if node.tag.split('}')[1] == 'g':
    for child in node:
      walk(child)

def checkStyle(node):
  styles = ss.parseStyle(node.get('style'))
  for c in range(len(colortags)):
    if colortags[c] in styles.keys():
      palette.append(styles[colortags[c]])

class C(inkex.Effect):
  def effect(self):
    '''
    TODO:
    '''
    if len(self.options.ids) < 1:
      inkex.errormsg("Plz, Select something.")
      exit()
    osb = 'http://www.openswatchbook.org/uri/2009/osb'
    svg = self.document.getroot()
    defs = self.xpathSingle('//svg:defs')
    for id,node in self.selected.iteritems():
      walk(node)
    msg = "Empty result"
    if len(pallete) > 0:
      for clr in palette:
        lgSwatch = inkex.etree.SubElement(defs,inkex.addNS('linearGradient','svg'))
        lgSwatch.set('id','sw' + clr)
        lgSwatch.set(inkex.etree.QName(osb,'paint'),'solid')
        lgStop = inkex.etree.SubElement(lgSwatch,inkex.addNS('stop','svg'))
        lgStop.set('stop-color',clr)
        lgSwatch.append(lgStop)
        defs.append(lgSwatch)
      msg = "Generated palette: " + ",".join(palette)
    inkex.debug( msg )

c = C()
c.affect()

