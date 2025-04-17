const panels = document.querySelectorAll(".panel");

panels.forEach(panel => {
    panel.addEventListener("click", () => {
        const rect = panel.getBoundingClientRect();

        const clone = panel.cloneNode(true);
        clone.classList.add("animated-clone");

        //set initial dimension
        clone.style.top = `${rect.top}px`;
        clone.style.left = `${rect.left}px`;
        clone.style.width = `${rect.width}px`;
        clone.style.height = `${rect.height}px`;

        //Add a close button
        const closeBtn = document.createElement('button');
        closeBtn.classList.add("close-btn");
        closeBtn.innerText = 'X';
        clone.appendChild(closeBtn);

        document.body.appendChild(clone);

        //force reflow
        clone.getBoundingClientRect()

        //animate to fullscreen
        clone.style.top = `0px`;
        clone.style.left = `0px`;
        clone.style.width = `100vw`;
        clone.style.height = `100vh`;

        closeBtn.addEventListener("click", (e) => {
            e.stopPropagation();

            //animate back to original
            clone.style.top = `${rect.top}px`;
            clone.style.left = `${rect.left}px`;
            clone.style.width = `${rect.width}px`;
            clone.style.height = `${rect.height}px`;

            clone.addEventListener("transitionend", () => {
                clone.remove()
            }, {once: true});
        });
    });
});