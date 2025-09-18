import L from "leaflet";

const createIcon = (iconFileName, size = 30) =>
  new L.Icon({
    iconUrl: process.env.PUBLIC_URL + `/image/${iconFileName}`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size],
    popupAnchor: [0, -size + 2],
  });

export const getFlagIcon = () => createIcon("red.png");
export const getHoverIcon = () => createIcon("red.png");
export const yellowFlagIcon = () => createIcon("yellow.png");
export const RainIcon = () => createIcon("rain.png");
export const WindIcon = () => createIcon("wind.png");
export const RainWindIcon = () => createIcon("rain_wind.png");
