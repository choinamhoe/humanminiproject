import { GeoJSON } from "react-leaflet";

const CustomGeoMap = ({
  data,
  handleClick,
  handleMouseOver,
  handleMouseOut,
}) => {
  // 기본 스타일
  const geoStyle = {
    color: "#204172ff",
    weight: 2,
    fillColor: "#204172ff",
    fillOpacity: 0.4,
  };
  const onEachFeature = (feature, layer) => {
    // ✅ feature 객체에 layer 저장
    feature.layer = layer;

    // 이벤트 등록
    layer.on({
      mouseover: (e) => handleMouseOver(feature, e),
      mouseout: (e) => handleMouseOut(feature, e),
      click: (e) => handleClick && handleClick(feature, e),
    });
  };

  return <GeoJSON data={data} style={geoStyle} onEachFeature={onEachFeature} />;
};

export default CustomGeoMap;
