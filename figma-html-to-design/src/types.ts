export interface RGBAColor {
  r: number;
  g: number;
  b: number;
  a: number;
}

export interface ElementData {
  tagName: string;
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  backgroundColor: RGBAColor;
  borderRadius: number;
  borderWidth: number;
  borderColor: RGBAColor;
  opacity: number;
  // Text
  text: string | null;
  fontSize: number;
  fontFamily: string;
  fontWeight: string;
  fontStyle: string;
  color: RGBAColor;
  lineHeight: number;
  letterSpacing: number;
  textAlign: string;
  textDecoration: string;
  // Layout
  display: string;
  overflow: string;
  boxShadow: string;
  // Image (base64 data URL)
  imageData?: string;
  // Children
  children: ElementData[];
}

export type PluginMessage =
  | { type: 'import-html'; elements: ElementData[]; canvasWidth: number; canvasHeight: number; renderWidth: number }
  | { type: 'error'; message: string }
  | { type: 'success'; message: string }
  | { type: 'notify'; message: string };
