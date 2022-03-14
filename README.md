# Hugo Basics

## Layout

Hugo 的頁面是用許多個 layout 組合起來的
```
.
├── 404.html
├── about
│   └── list.html
├── contact
│   └── list.html
├── _default
│   ├── baseof.html     # 最外層的 layout
│   ├── list.html       # 列表頁面
│   ├── post.html       # 兩種不同的單頁
│   └── single.html     # 兩種不同的單頁
├── index.html          # 首頁
├── partials
│   ├── client-slider.html
│   ├── footer.html
│   ├── header.html     # nav bar
│   ├── head.html
│   ├── page-title.html
│   └── preloader.html
└── portfolio
    ├── list.html
    └── single.html
```


`layouts/` 或 `themes/[your-theme]/layouts`，如果要改 layout，請把它複製到外面再改，不要動 themes 底下的檔案。

### 建立 partial

https://gohugo.io/templates/partials/

把檔案放在 `layouts/partials/*<PARTIALNAME>.html`，然後在其他 layout 裡寫 `{{ partial "<PATH>/<PARTIAL>.html" . }}`

### 填老師資料

打開 `layouts/about/list.html` 可以看到裡面的資料是來自 site.Data.about.team，site.Data 就是放在 data/ 底下的 xml，

### 填課程資料

建立新課程：
```
hugo new courses/國文.md
```
會建立 `content/courses/國文.md`，編輯此檔案來放入課程資訊

建議可以寫個爬蟲省時間


## Git 常用指令

```
git status
git log
git add .                   # 把檔案加入 git 追蹤清單
git commit -m "message"

# 每次開始寫之前先跑
git pull                    # 把遠端更新拉到本地

# 每次寫完後跑
git push origin main        # 把本地更新推到遠端
```
