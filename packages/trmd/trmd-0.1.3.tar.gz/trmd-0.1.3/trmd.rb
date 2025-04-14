class Trmd < Formula
  include Language::Python::Virtualenv

  desc "Translate Markdown using OpenAI"
  homepage "https://github.com/rioriost/homebrew-trmd/"
  url "https://files.pythonhosted.org/packages/8f/09/537e6e1f16ca82c5447c124794ecda8d3b60dcefea6eadcffd2c8674bc8b/trmd-0.1.2.tar.gz"
  sha256 "e7dd6184002cd4fa06ea2bc8fafcb05df0960754fecaf3f07e5448a407487e35"
  license "MIT"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
    system libexec/"bin/python", "-m", "pip", "install", "openai"
  end

  test do
    system "#{bin}/trmd", "--help"
  end
end
