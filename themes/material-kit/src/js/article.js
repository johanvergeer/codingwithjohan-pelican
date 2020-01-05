// Use a button to scroll to the main section of the article
const btnScrollToArticle = document.getElementById('btnScrollToArticle');
btnScrollToArticle.addEventListener("click", () => {
    const article = document.getElementById("article");
    article.scrollIntoView({behavior: 'smooth', block: "start"})
});