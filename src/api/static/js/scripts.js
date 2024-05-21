/* ABRE E FECHA MENU LATERAL EM MODO MOBILE */

const menuMobile = document.querySelector(".menu-mobile");
const body = document.querySelector("body");

menuMobile.addEventListener("click", () => {
    menuMobile.classList.contains("bi-list")
        ? menuMobile.classList.replace("bi-list", "bi-x")
        : menuMobile.classList.replace("bi-x", "bi-list");
    body.classList.toggle("menu-nav-active");
});

/* ATIVAR CARREGAMENTO DO BOTÃO ENVIAR */

const btnEnviar = document.querySelector('#btn-enviar')
const btnenviarLoader = document.querySelector('#btn-enviar-loader')

btnEnviar.addEventListener("click", ()=>{
    btnenviarLoader.style.display = "block";
    btnEnviar.style.display = "none"
})

/* TIRAR MENSAGEM EMAIL */
setTimeout(() => {
    document.querySelector('#alerta').style.display = 'none';
}, 3000)