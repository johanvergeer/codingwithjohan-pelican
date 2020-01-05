// Use a button to scroll to the main section of the article
const btnScrollToArticle = document.getElementById('btnScrollToArticles');
btnScrollToArticle.addEventListener("click", () => {
    const article = document.getElementById("articles");
    article.scrollIntoView({behavior: 'smooth', block: "start"})
});