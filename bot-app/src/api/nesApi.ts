// Utility for communicating with the NES emulator RAM

export async function getRamContents() {
  const ram_contents_resource = await fetch('/symlinks/ramdisk/ram_contents.json');
  const ram_contents = await ram_contents_resource.json();
  return ram_contents;
}
