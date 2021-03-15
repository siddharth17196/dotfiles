"                        _
" | '_ \ / _ \/ _ \ \ / / | '_ ` _ \
"  _ __   ___  _____   _(_)_ __ ___
" | '_ \ / _ \/ _ \ \ / / | '_ ` _ \
" | | | |  __/ (_) \ V /| | | | | | |
" |_| |_|\___|\___/ \_/ |_|_| |_| |_|

" ===========================================================================
" # Editor Settings
" ===========================================================================
syntax on
set hidden
set noerrorbells
set tabstop=4 softtabstop=4
set shiftwidth=4
set expandtab
set smartindent
set nu              " line numbers
set relativenumber  " relative line numbers"
set nowrap
set smartcase
set noswapfile
set nobackup
" set undodir=~/.vim/undodir
set undofile
set incsearch
set scrolloff=8
set signcolumn=yes
" set clipboard=unnamedplus
" set termguicolors
" For better display of messages
set cmdheight=2

" Having longer updatetime (default is 4000 ms = 4 s) leads to noticeable
" delays and poor user experience.
set updatetime=100

" Don't pass messages to |ins-completion-menu|.
set shortmess+=c

filetype plugin on
filetype plugin indent on

set colorcolumn=80
highlight ColorColumn ctermbg=0 guibg=lightgrey




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

" github
Plug 'tpope/vim-fugitive'

" fuzzy finder
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'

" language support for golang
Plug 'fatih/vim-go', { 'do': ':GoUpdateBinaries' }

" C/C++ code formater
Plug 'rhysd/vim-clang-format'
Plug 'jiangmiao/auto-pairs'

" tagbar
Plug 'preservim/tagbar'

" nerdtree
Plug 'preservim/nerdtree'

" coc intellisense
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'wakatime/vim-wakatime'

call plug#end()



" ===========================================================================
" # Global variables
" ===========================================================================

" For a retro colorscheme 'bg' can be light/dark
colorscheme gruvbox
set background=dark
set t_Co=256
let g:gruvbox_hls_cursor='orange'
" highlight Normal ctermfg=252 ctermbg=none

"fzf layout
let g:fzf_layout = {'up':'~90%', 'window': { 'width': 0.8, 'height': 0.8,'yoffset':0.5,'xoffset': 0.5, 'highlight': 'Todo', 'border': 'sharp' } }

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

" Trigger configuration. Do not use <tab> if you use any autocomplete
let g:UltiSnipsExpandTrigger="<c-a>"
let g:UltiSnipsJumpForwardTrigger="<c-b>"
let g:UltiSnipsJumpBackwardTrigger="<c-z>"



" ===========================================================================
" # Key Mappings
" ===========================================================================

" NerdTree toggler
map <leader>t :NERDTreeToggle<CR>
" Close nvim if only nerdtree is open
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif

"tagbar toggler
nmap <leader>q :TagbarToggle<CR>

" Copy to clipboard (xclip reqd)
vnoremap <leader>c :w !xclip -i -sel c<CR>

" vertical resize
nnoremap <silent> <leader>= :vertical resize +5<CR>
nnoremap <silent> <leader>- :vertical resize -5<CR>



" Use tab for trigger completion with characters ahead and navigate.
" NOTE: Use command ':verbose imap <tab>' to make sure tab is not mapped by
" other plugin before putting this into your config.
inoremap <silent><expr> <TAB>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()
inoremap <expr><S-TAB> pumvisible() ? "\<C-p>" : "\<C-h>"

function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

" Use <c-space> to trigger completion.
if has('nvim')
  inoremap <silent><expr> <c-space> coc#refresh()
else
  inoremap <silent><expr> <c-@> coc#refresh()
endif

" Use `[g` and `]g` to navigate diagnostics
" Use `:CocDiagnostics` to get all diagnostics of current buffer in location list.
nmap <silent> [g <Plug>(coc-diagnostic-prev)
nmap <silent> ]g <Plug>(coc-diagnostic-next)

" GoTo code navigation.
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)


" ===========================================================================
" # Functions
" ===========================================================================

" function to trim white spaces
fun! TrimWhitespace()
    let l:save = winsaveview()
    keeppatterns %s/\s\+$//e
    call winrestview(l:save)
endfun

augroup THE_PRIMEAGEN
    autocmd!
    autocmd BufWritePre * :call TrimWhitespace()
augroup END
