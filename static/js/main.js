let total = {};
let pageObj = {
    page: null,
    page_truck: null
};
getParamFromQuery('page');
getParamFromQuery('page_truck');
   
async function getParamFromQuery(name) {
    const params = document.location.href.split('?')[1];
    const qury = new URLSearchParams(params);
    const param = parseInt(qury.get(name));
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
    const clearUrl = document.location.href.split('?')[0];
    page = param.page;
    pageTruck = param.page_truck;
    let newUrl = clearUrl;
    
    if (page || pageTruck) {
        newUrl = newUrl + '?' + (page ? `page=${page}` : `page_truck=${pageTruck}`);
    }
    if (page && pageTruck) {
        newUrl = `${newUrl}&page_truck=${pageTruck}`
    }
    if (document.location.href !== newUrl) {
        document.location.href = newUrl;
    }
}