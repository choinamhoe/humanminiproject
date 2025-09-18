const backgrounds = [
  `${process.env.PUBLIC_URL}/video/firstpage.avif`,
  `${process.env.PUBLIC_URL}/video/background.avif`,
];

const texts = [
  {
    content: "골프장의 하늘을 미리 보는,",
    highlight: "swing sky",
    position: { top: "23%", right: "10%" },
  },
  {
    content: "날씨를 알고, 완벽한 라운드를 즐기다.",
    highlight: "",
    position: { top: "70%", left: "10%" },
  },
];
const logo = `${process.env.PUBLIC_URL}/image/logo.png`;

// named export
export { backgrounds, texts, logo };
