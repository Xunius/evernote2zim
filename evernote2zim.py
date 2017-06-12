'''Convert evernote docs to zim wiki.

This is achieved by:
    1. Export your evernote docs to html and save to a folder (<HTML_DIR>).
    2. Convert html to markdown by using the html2text module.
    3. Convert markdown to zim-wiki syntax using the markdown2zim module, and
       save to a given folder <ZIM_DIR>.
    4. Copy over attched images to <ZIM_DIR>.
    5. In zim desktop, create a new notebook, this will create a new folder
       in your drive. Close the new notebook and go into that folder,
       and copy over the stuff (.txt files and attachment folders)
       to this new folder.
    6. Open the new notebook again to see the final result.

Step 2-4 is done by this script. Other step should be done by the user.

Some tips:
    * After creating the new notebook, you can let it stay open, and
      copy over the docs, then use Tools -> Update index to let
      it refresh.
    * Sometimes after the above the HOME page is gone, try restarting
      zim.
    * When exporting your docs from Evernote, right click a notebook to
      export the entire notebook.

Author: guangzhi XU (xugzhi1987@gmail.com; guangzhi.xu@outlook.com)
Update time: 2017-06-12 21:23:43.

'''
import os,sys
import re
import shutil
from lib import html2text
from lib.markdown2zim import Markdown2Zim
import datetime
import argparse

__version__='evernote2zim v0.1'



def deu(text):
    if isinstance(text,str):
        return text.decode('utf8','replace')
    else:
        return text

def enu(text):
    if isinstance(text,unicode):
        return text.encode('utf8','replace')
    else:
        return text


# these chars are invalid zim titles
invalid_chars=re.compile(r'([#%*_|\<>/?"])', re.X | re.U | re.M)

# search links in the form [link](shortended url)
_link_def_re = re.compile(r"""
    \[(.+?)\]            # id = \1
    \((.+?)\)           # url = \2
    """, re.X | re.M | re.U)

def invalidSub(match):
    if match.group(1)=='%':
        return ' percent'
    elif match.group(1)=='"':
        return "''"
    else:
        return ''


def main(args):

    html_dir,zim_dir=args

    html_dir=os.path.expanduser(html_dir)
    html_dir=os.path.abspath(html_dir)

    zim_dir=os.path.expanduser(zim_dir)
    zim_dir=os.path.abspath(zim_dir)

    if not os.path.exists(zim_dir):
        print('\n# <evernote2zim>: Create folder: %s' %zim_dir)
        os.makedirs(zim_dir)

    #----------------Loop through files----------------
    titles=[]
    for ff in os.listdir(html_dir):

        basename,ext=os.path.splitext(ff)
        if ext!='.html':
            continue

        #-----------------Skip index files-----------------
        if '_index.html' in ff:
            continue

        file_in_path=os.path.join(html_dir,ff)
        print('# <evernote2zim>: Converting file: %s' %ff)

        with open(file_in_path,'r') as fin:

            lines=''.join(fin.readlines())
            lines=deu(lines)

            #-------------Convert html to markdown-------------
            h=html2text.HTML2Text()
            mdtext=h.handle(lines)

            #-------Remove the weird %20 in index files-------
            mdtext=mdtext.replace(u'%20',' ')
            mdtext=mdtext.replace(u'.html','')

            #------------------Get full title------------------
            title=mdtext.split('\n')[0]

            #-------------Filter out invalid chars-------------
            title=invalid_chars.sub('',title).strip()
            title=title.replace(' ','_')
            titles.append(title)

            #-------------Convert markdown to zim-------------
            zimtext=Markdown2Zim().convert(mdtext)
            
            #-------------------Save output-------------------
            file_out_name='%s.txt' %title
            file_out_path=os.path.join(zim_dir,file_out_name)

            with open(file_out_path,'w') as fout:
                zimtext=enu(zimtext)
                fout.write(zimtext)

            #------------------Copy img files------------------
            img_dir=os.path.join(html_dir,'%s_files' %basename)
            if os.path.exists(img_dir):
                target_img_dir=os.path.join(zim_dir,title)
                shutil.copytree(img_dir,target_img_dir)

    #---------------Create an index page---------------
    index_str=u'====== Home ======\nCreated %s\n\n' \
            % datetime.datetime.now().strftime('%A %d %h %Y')

    titles.sort()
    for tt in titles:
        strtt=u'* [[:%s|%s]]\n' %(tt,tt)
        index_str=index_str+strtt

    file_out_name='Home.txt'
    file_out_path=os.path.join(zim_dir,file_out_name)

    with open(file_out_path,'w') as fout:
        index_str=enu(index_str)
        fout.write(index_str)

    return 0


if __name__=='__main__':


    parser = argparse.ArgumentParser(description=\
            'Convert Evernote export to zim-wiki syntax.')

    parser.add_argument('indir', type=str,\
            help='Folder storing exported html files from Evernote.')
    parser.add_argument('outdir', type=str,\
            help='Target folder to save the result.')

    try:
        args = parser.parse_args()
    except:
        sys.exit(1)

    main((args.indir,args.outdir))








    


