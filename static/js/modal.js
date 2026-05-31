/*
   modal.js — DEACTIVATED for Editorial Engine v2.0
   
   Card click listeners have been moved to page-news.js and page-articles.js.
   Navigation now uses window.location.href = '/news/' + id.
   
   The modal overlay HTML is kept in the templates for backward compatibility
   but is no longer triggered by card clicks.
   
   YouTube embed helper is preserved below for any future use.
*/

window.PEBModal = (function () {
  // DEACTIVATED: Modal-based card navigation is disabled.
  // Cards now navigate directly to detail_view pages.
  // See page-news.js and page-articles.js for new navigation logic.

  // HELPER: Converts any YouTube link to the /embed/ version (preserved for re-use)
  function getYoutubeEmbedUrl(url) {
    if (!url) return null;
    let videoId = "";
    if (url.includes("v=")) {
      videoId = url.split("v=")[1].split("&")[0];
    } else if (url.includes("youtu.be/")) {
      videoId = url.split("youtu.be/")[1].split("?")[0];
    } else if (url.includes("shorts/")) {
      videoId = url.split("shorts/")[1].split("?")[0];
    } else if (url.includes("embed/")) {
      return url;
    }
    return videoId ? `https://www.youtube.com/embed/${videoId}` : url;
  }

  return {
    getYoutubeEmbedUrl,
    // Stub methods — no-ops to avoid errors if called from old code
    openNews: function () { console.warn("PEBModal.openNews: deactivated. Use /news/<id> navigation."); },
    openArticle: function () { console.warn("PEBModal.openArticle: deactivated. Use /articles/<id> navigation."); },
    close: function () {},
  };
})();
