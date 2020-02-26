" Will's super custom .vimrc
" --------------------------
" Created: 2018-04-03
" Updated: 2019-05-02

" Disable splash
set shortmess=I

" Visual
colorscheme industry
set guifont=Monospace\ 10.5
syntax enable
set number
set showcmd
set cursorline
filetype indent on
set wildmenu
set lazyredraw
set showmatch
set formatoptions=l
set lbr
set spell spelllang=en_au

" Tabbing
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set autoindent
set smartindent

" Searching
set incsearch
set hlsearch

" Code
set autoindent

" Keyboard
noremap <Up> <NOP>
noremap <Down> <NOP>
noremap <Left> <NOP>
noremap <Right> <NOP>

inoremap kj <Esc>
inoremap KJ <Esc>

" Commands
command! WipeReg for i in range(34,122) | silent! call setreg(nr2char(i), []) | endfor

autocmd VimEnter * WipeReg
