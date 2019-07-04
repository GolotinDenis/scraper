$(document).ready(function () {
    pageObj = {
        page: getParamFromQuery('page'),
        pageTruck: getParamFromQuery('pageTruck')
    }
});
let pageObj = {
   
}

let total = 10;
function setUrl(param) {
    let clearUrl = document.location.href.split('?')[0];
    page = param.page;
    pageTruck = param.pageTruck;
    let newUrl = clearUrl;
    if (page || pageTruck) {
        newUrl = newUrl + '?' + (page ? `page=${page}` : `pageTruck=${pageTruck}`);
    }
    if (page && pageTruck) {
        newUrl = `${newUrl}&pageTruck=${pageTruck}`
    }
    if (document.location.href !== newUrl) {
        document.location.href = newUrl;
    }
}
function navigateToPage(icrement, name) {
    if(pageObj[name] + icrement<0) {
        return;
    }
    pageObj[name] = pageObj[name] + icrement;

    setUrl(pageObj);
}
function getParamFromQuery(name) {
    let params = document.location.href.split('?')[1];
    let qury = new URLSearchParams(params);
    let param = parseInt(qury.get(name));
    return isNaN(param) ? '' : param > total ? total : param;
}