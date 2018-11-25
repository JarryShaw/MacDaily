class Macdaily < Formula
  include Language::Python::Virtualenv

  desc "macOS Automated Package Manager"
  homepage "https://github.com/JarryShaw/MacDaily#macdaily"
  url "https://files.pythonhosted.org/packages/96/80/a70a7e939bb179aecd602be61ab8cb423bfe370f272caa3802e5374d3cee/macdaily-2018.11.23a2.tar.gz"
  sha256 "d8070e1f9070a6cb9cc4acd1ea313b8155c00ded29b3b188315c9d4ef808491f"

  depends_on "python3"

  def install
    virtualenv_create(libexec, "python3")
    virtualenv_install_with_resources
  end

  test do
    false
  end
end
