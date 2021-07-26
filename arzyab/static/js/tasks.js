const openMenu = () => {
  document.getElementById("container").style.display = "flex";
  document.getElementById("menu").style.display = "flex";
  document.getElementById("openMenuBtn").style.display = "none";

  if (window.innerWidth <= 960) {
    document.getElementById("tradeTable").style.gridTemplateColumns = "1fr";
  }
};

const closeMenu = () => {
  document.getElementById("container").style.removeProperty("display");
  document.getElementById("menu").style.removeProperty("display");
  document.getElementById("openMenuBtn").style.removeProperty("display");

  document.getElementById("tradeTable").style.gridTemplateColumns =
    "repeat(2, minmax(0, 1fr))";
};

const changeTab = (e) => {
  let length = document
    .getElementById("projectsNav")
    .getElementsByTagName("a").length;

  for (let i = 0; i < length; i++) {
    document
      .getElementById("projectsNav")
      .getElementsByTagName("a")
      .item(i)
      .classList.remove("selected");
  }

  e.target.classList.add("selected");
};

const taskPopup_open = () => {
  document.getElementById("taskPopup").style.display = "flex";
  document.getElementById("page-mask").style.display = "block";
};

const taskPopup_close = () => {
  document.getElementById("taskPopup").style.display = "none";
  document.getElementById("page-mask").style.display = "none";
};

const projectPopup_open = () => {
  document.getElementById("projectPopup").style.display = "flex";
  document.getElementById("page-mask").style.display = "block";
};

const projectPopup_close = () => {
  document.getElementById("projectPopup").style.display = "none";
  document.getElementById("page-mask").style.display = "none";
};

// const task_done = (e) => {  };

const task_undone = (e) => {};
