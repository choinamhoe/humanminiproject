import { useEffect, useState, useRef } from "react";
import { MapContainer, TileLayer, Marker } from "react-leaflet";

import "leaflet/dist/leaflet.css";
import "../css/mapview.css";
import {
  RainWindIcon,
  RainIcon,
  WindIcon,
  yellowFlagIcon,
  getFlagIcon,
} from "../constants/GeoIcons";
import CustomGeoMap from "./CustomGeoMap";
import GolfPopup from "./GolfPopup";
import AreaNormalizer from "./AreaNormalizer";
const LeafletMap = ({
  pointsData,
  selectedData,
  setSelectedData,
  setSearchTerm,
  selectedPoint,
  setSelectedPoint,
  onClickDetail,
  geoData,
}) => {
  const mapRef = useRef(null);

  const [centerPoint, setCenterPoint] = useState([37.5665, 126.978]);
  const [selectedLayerName, setSelectedLayerName] = useState(null);

  const handleMouseOver = (feature, e) => {
    const layer = e?.target;
    if (!layer) return;

    layer.setStyle({
      weight: 3,
      color: "#f7f3f3ff",
    });
  };

  const handleMouseOut = (feature, e) => {
    const layer = e?.target;
    if (!layer) return;

    layer.setStyle({
      color: "#204172ff",
      weight: 2,
    });
  };
  const handleMapClick = (feature, e) => {
    const layer = e?.target;
    if (!layer) return;
    //   // const layerBounds = layer.getBounds();
    //   // const center = layerBounds.getCenter();
    const center = e.latlng;
    const centerList = [center.lat, center.lng];
    const areaName = AreaNormalizer(feature.properties.CTP_KOR_NM);
    setSelectedLayerName(areaName);
    setCenterPoint(centerList);
    setSearchTerm("");
    if (mapRef.current) {
      mapRef.current.setView(centerList, 9);
    }
  };

  useEffect(() => {
    if (!selectedLayerName || pointsData.length === 0) return;
    const filtered = pointsData.filter((item) =>
      item.area.includes(selectedLayerName)
    );
    setSelectedData(filtered);
  }, [selectedLayerName, pointsData]);
  return (
    <MapContainer
      center={centerPoint}
      ref={mapRef}
      zoom={7}
      className="map-container"
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      {selectedData.length > 0 &&
        selectedData.map((item, idx) => (
          <Marker
            key={idx}
            position={[item.Latitude, item.Longitude]}
            icon={
              Number(item.RN) >= 1 && Number(item.WS) >= 10
                ? RainWindIcon()
                : Number(item.RN) >= 1
                ? RainIcon()
                : Number(item.WS) >= 10
                ? WindIcon()
                : selectedPoint?.id === item.id
                ? yellowFlagIcon()
                : getFlagIcon()
            }
            eventHandlers={{
              click: () => setSelectedPoint(item),
            }}
          >
            <GolfPopup item={item} onClickDetail={onClickDetail} />
          </Marker>
        ))}
      {geoData && (
        <CustomGeoMap
          data={geoData}
          handleClick={handleMapClick}
          handleMouseOver={handleMouseOver}
          handleMouseOut={handleMouseOut}
        />
      )}
    </MapContainer>
  );
};

export default LeafletMap;
