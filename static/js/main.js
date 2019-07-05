$(document).ready(function () {
    total = {};
    getParamFromQuery('page');
    getParamFromQuery('pageTruck');
    pageObj = {
        page: null,
        pageTruck: null
    }    
    
    
});
async function getParamFromQuery(name) {
    let params = document.location.href.split('?')[1];
    let qury = new URLSearchParams(params);
    let param = parseInt(qury.get(name));
    total = await $.ajax({
        url: '/api/count',
        method: 'GET'
    })
    pageObj[name] = isNaN(param) ? '' : param > total[name] ? total[name] : param;
}
function navigateToPage(icrement, name) {
    if (pageObj[name] + icrement < 0) {
        return;
    }
    pageObj[name] = pageObj[name] + icrement > total[name] ? total[name] : pageObj[name] + icrement;

    setUrl(pageObj);
}

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