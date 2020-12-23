"        _                    
" __   _(_)_ __ ___  _ __ ___ 
" \ \ / / | '_ ` _ \| '__/ __|
"  \ V /| | | | | | | | | (__ 
"   \_/ |_|_| |_| |_|_|  \___|


syntax on
" ===========================================================================
" # Editor Settings 
" ===========================================================================
set hidden
set noerrorbells
set tabstop=4 softtabstop=4
set shiftwidth=4
set expandtab
set smartindent
set number          " line numbers
set relativenumber  " relative line numbers"
set nowrap
set smartcase
set noswapfile
set nobackup
set nocompatible
set undodir=~/.vim/undodir
set undofile
set incsearch
" set clipboard=unnamedplus
" set termguicolors
" For better display of messages
set cmdheight=2

filetype plugin on
filetype plugin indent on

" Having longer updatetime (default is 4000 ms = 4 s) leads to noticeable
" delays and poor user experience.
set updatetime=100

" Don't pass messages to |ins-completion-menu|.
set shortmess+=c

set colorcolumn=80
highlight ColorColumn ctermbg=0 guibg=lightgrey
" set nocompatible              " required
" syntax enable
" filetype indent on
" set autoindent
" filetype off                  " required

" Color scheme
" mkdir -p ~/.vim/colors && cd ~/.vim/colors
" wget -O wombat256mod.vim http://www.vim.org/scripts/download_script.php?src_id=13400
" set t_Co=256
" color wombat256mod

" hi CursorLineNR cterm=bold
" augroup CLNRSet
"     autocmd! ColorScheme * hi CursorLineNR cterm=bold
" augroup END


" ===========================================================================
" YCM (using vundle)
" ===========================================================================
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
Plugin 'Valloric/YouCompleteMe'
Plugin 'tpope/vim-fugitive'
Plugin 'wakatime/vim-wakatime'
call vundle#end()
filetype plugin indent on


" ===========================================================================
" # Vim Plugins (using plugs)
" ===========================================================================
call plug#begin()
" Plug 'roxma/nvim-completion-manager'
Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'

" tabular plugin is used to format tables
Plug 'godlygeek/tabular'
" JSON front matter highlight plugin
Plug 'elzr/vim-json'
" Markdown
Plug 'plasticboy/vim-markdown'
Plug 'iamcco/markdown-preview.nvim', { 'do': { -> mkdp#util#install() }, 'for': ['markdown', 'vim-plug']}

" theme and powerline
Plug 'morhetz/gruvbox'
Plug 'vim-airline/vim-airline'

" commenting 
Plug 'tpope/vim-commentary'

" multiple cursors (as in sublime)
Plug 'terryma/vim-multiple-cursors'

" code folding 'zc/zC' and 'zo/zO'
Plug 'tmhedberg/SimpylFold'

" github 
" Plug 'tpope/vim-fugitive'

" fuzzy finder 
Plug 'ctrlpvim/ctrlp.vim'

Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'

" language support for golang
Plug 'fatih/vim-go', { 'do': ':GoUpdateBinaries' }

" VimWiki
Plug 'vimwiki/vimwiki'

" C/C++ code formater 
Plug 'rhysd/vim-clang-format'

Plug 'jiangmiao/auto-pairs'

" nerdtree
Plug 'preservim/nerdtree'

call plug#end()

" let g:deoplete#enable_at_startup = 1
" For a retro colorscheme 'bg' can be light/dark
colorscheme gruvbox
set background=dark
set t_Co=256
let g:gruvbox_hls_cursor='orange'
" highlight Normal ctermfg=252 ctermbg=none


" disable header folding
let g:vim_markdown_folding_disabled = 1

" do not use conceal feature, the implementation is not so good
let g:vim_markdown_conceal = 0

" disable math tex conceal feature
let g:tex_conceal = ""
let g:vim_markdown_math = 1

" support front matter of various format
let g:vim_markdown_frontmatter = 1  " for YAML format
let g:vim_markdown_toml_frontmatter = 1  " for TOML format
let g:vim_markdown_json_frontmatter = 1  " for JSON format

" github markdown 
let g:mkdp_refresh_slow=1
let g:mkdp_markdown_css='home/siddharth/.vim/gh_markdown.css'
let g:mkdp_browser = 'brave'

let g:vimwiki_list = [{'path': '~/vimwiki/', 'syntax': 'markdown', 'ext': '.md'}]
let g:vim_markdown_auto_extension_ext = 'md'

augroup markdown
    au!
    au BufNewFile,BufRead *.vimwiki, *.wiki, *.md, *.markdown setlocal filetype=markdown
augroup END

" NerdTree toggler
map <leader>t :NERDTreeToggle<CR>
" Close nvim if only nerdtree is open
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif

" Copy to clipboard (xclip reqd)
vnoremap <leader>c :w !xclip -i -sel c<CR>

nnoremap <silent> <leader>= :vertical resize +5<CR>
nnoremap <silent> <leader>- :vertical resize -5<CR>

" Trigger configuration. Do not use <tab> if you use https://github.com/Valloric/YouCompleteMe.
let g:UltiSnipsExpandTrigger="<c-a>"
let g:UltiSnipsJumpForwardTrigger="<c-b>"
let g:UltiSnipsJumpBackwardTrigger="<c-z>"


function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

" Function for YCM
" fun! GoYCM()
nnoremap <leader>gd :YcmCompleter GoTo<CR>
nnoremap <leader>gr :YcmCompleter GoToReferences<CR>
nnoremap <leader>rr :YcmCompleter RefactorRename<space>
" endfun
