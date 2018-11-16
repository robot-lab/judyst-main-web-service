<template>
    <p><!--Nothing--></p>
</template>




<script>
export default {
    name: "FooterController",
    created: function () {
        document.getElementsByClassName("footer").style.position = "relative";
        
    },
    destroyed: function () {
        document.getElementsByClassName("footer").style.position = "absolute";
        
    }
}
</script>



