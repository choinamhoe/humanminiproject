const AreaNormalizer = (name) => {
  if (!name) return "";
  return name
    .replace("세종특별자치시", "세종")
    .replace("특별자치도", "")
    .replace("광역시", "")
    .replace("특별시", "")
    .replace("자치시", "")
    .replace("충청북", "충북")
    .replace("충청남", "충남")
    .replace("전라북", "전북")
    .replace("전라남", "전남")
    .replace("경상북", "경북")
    .replace("경상남", "경남")
    .replace("도", "")
    .replace("시", "")
    .trim();
};

export default AreaNormalizer;
